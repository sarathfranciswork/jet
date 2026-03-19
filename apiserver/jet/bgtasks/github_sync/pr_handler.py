"""PR automation — link PRs to issues, trigger state changes."""
import logging

from celery import shared_task
from django.utils import timezone
from sentry_sdk import capture_exception

from jet.db.models import (
    Issue,
    IssueLink,
    GithubPullRequest,
    GithubRepositorySync,
    GithubSyncConfig,
)
from jet.utils.integrations.github import GithubAPIClient
from .reference_parser import parse_issue_references, resolve_issue_reference
from .state_sync import get_jet_state_for_pr_state
from .conflict_resolver import log_sync

logger = logging.getLogger(__name__)


@shared_task
def handle_pull_request_event(repository_sync_id, pr_data, action):
    """
    Handle a pull_request webhook event.

    Actions: opened, closed, merged, reopened, converted_to_draft, ready_for_review
    """
    try:
        repository_sync = GithubRepositorySync.objects.select_related(
            "repository", "workspace_integration", "sync_config"
        ).get(id=repository_sync_id)
    except GithubRepositorySync.DoesNotExist:
        return

    try:
        sync_config = repository_sync.sync_config
    except GithubSyncConfig.DoesNotExist:
        return

    if not sync_config.is_active:
        return

    pr_number = pr_data.get("number")
    github_pr_id = pr_data.get("id")
    pr_title = pr_data.get("title", "")
    pr_body = pr_data.get("body") or ""
    pr_url = pr_data.get("html_url", "")
    is_merged = pr_data.get("merged", False)
    is_draft = pr_data.get("draft", False)

    # Determine PR state
    if is_merged:
        pr_state = "merged"
    elif pr_data.get("state") == "closed":
        pr_state = "closed"
    elif is_draft:
        pr_state = "draft"
    else:
        pr_state = "open"

    # Parse issue references from title and body
    text_to_parse = f"{pr_title}\n{pr_body}"
    bracket_refs, bare_refs = parse_issue_references(text_to_parse)

    try:
        if action == "opened":
            _handle_pr_opened(
                repository_sync, sync_config, pr_data, pr_state,
                bracket_refs, bare_refs,
            )
        elif action in ("closed", "reopened", "converted_to_draft", "ready_for_review"):
            _handle_pr_state_change(
                repository_sync, sync_config, pr_data, pr_state, action,
            )

        log_sync(
            repository_sync, "pull_request", github_pr_id, "github_to_jet", "success",
            payload={"action": action, "pr_number": pr_number, "state": pr_state},
        )
    except Exception as e:
        logger.exception(f"Error handling PR #{pr_number} event: {action}")
        log_sync(
            repository_sync, "pull_request", github_pr_id, "github_to_jet", "failed",
            error_message=str(e),
        )
        capture_exception(e)


def _handle_pr_opened(repository_sync, sync_config, pr_data, pr_state, bracket_refs, bare_refs):
    """Handle a newly opened PR — create records and link to issues."""
    pr_number = pr_data["number"]
    github_pr_id = pr_data["id"]
    pr_title = pr_data.get("title", "")
    pr_url = pr_data.get("html_url", "")
    author = pr_data.get("user", {})

    workspace_id = repository_sync.workspace_id

    # Process bracket refs (automation triggers)
    for ref in bracket_refs:
        issue = resolve_issue_reference(ref, workspace_id)
        if not issue:
            continue

        pr_record, created = GithubPullRequest.objects.update_or_create(
            repository_sync=repository_sync,
            pr_number=pr_number,
            defaults={
                "github_pr_id": github_pr_id,
                "title": pr_title,
                "url": pr_url,
                "state": pr_state,
                "is_draft": pr_data.get("draft", False),
                "issue": issue,
                "triggers_automation": True,
                "author_login": author.get("login", ""),
                "author_avatar_url": author.get("avatar_url", ""),
                "project_id": issue.project_id,
                "workspace_id": workspace_id,
            },
        )

        # Apply state mapping
        new_state = get_jet_state_for_pr_state(sync_config, pr_state)
        if new_state:
            issue.state = new_state
            issue.updated_by = repository_sync.actor
            issue.save(update_fields=["state", "updated_by", "updated_at"])

    # Process bare refs (link only)
    for ref in bare_refs:
        issue = resolve_issue_reference(ref, workspace_id)
        if not issue:
            continue

        pr_record, created = GithubPullRequest.objects.update_or_create(
            repository_sync=repository_sync,
            pr_number=pr_number,
            defaults={
                "github_pr_id": github_pr_id,
                "title": pr_title,
                "url": pr_url,
                "state": pr_state,
                "is_draft": pr_data.get("draft", False),
                "issue": issue,
                "triggers_automation": False,
                "author_login": author.get("login", ""),
                "author_avatar_url": author.get("avatar_url", ""),
                "project_id": issue.project_id,
                "workspace_id": workspace_id,
            },
        )

        # Create an IssueLink for bare refs
        IssueLink.objects.get_or_create(
            issue=issue,
            url=pr_url,
            defaults={
                "title": f"PR #{pr_number}: {pr_title}",
                "project_id": issue.project_id,
                "workspace_id": workspace_id,
                "created_by": repository_sync.actor,
                "updated_by": repository_sync.actor,
            },
        )


def _handle_pr_state_change(repository_sync, sync_config, pr_data, pr_state, action):
    """Handle PR state changes — update records and trigger issue state automation."""
    pr_number = pr_data["number"]
    is_merged = pr_data.get("merged", False)

    try:
        pr_record = GithubPullRequest.objects.select_related("issue").get(
            repository_sync=repository_sync, pr_number=pr_number
        )
    except GithubPullRequest.DoesNotExist:
        # PR wasn't tracked, try to handle it like a new PR
        text_to_parse = f"{pr_data.get('title', '')}\n{pr_data.get('body', '') or ''}"
        bracket_refs, bare_refs = parse_issue_references(text_to_parse)
        _handle_pr_opened(
            repository_sync, sync_config, pr_data, pr_state, bracket_refs, bare_refs
        )
        return

    # Update PR record
    pr_record.state = pr_state
    pr_record.is_draft = pr_data.get("draft", False)
    update_fields = ["state", "is_draft", "updated_at"]

    if is_merged:
        merged_at = pr_data.get("merged_at")
        if merged_at:
            pr_record.merged_at = merged_at
            update_fields.append("merged_at")

    if pr_data.get("state") == "closed" and not is_merged:
        closed_at = pr_data.get("closed_at")
        if closed_at:
            pr_record.closed_at = closed_at
            update_fields.append("closed_at")

    pr_record.save(update_fields=update_fields)

    # Apply state automation for bracket-ref PRs
    if pr_record.triggers_automation and pr_record.issue:
        new_state = get_jet_state_for_pr_state(sync_config, pr_state)
        if new_state:
            issue = pr_record.issue
            issue.state = new_state
            issue.updated_by = repository_sync.actor
            issue.save(update_fields=["state", "updated_by", "updated_at"])


@shared_task
def handle_pull_request_review_event(repository_sync_id, review_data, pr_data):
    """Handle pull_request_review.submitted event."""
    try:
        repository_sync = GithubRepositorySync.objects.select_related(
            "sync_config"
        ).get(id=repository_sync_id)
    except GithubRepositorySync.DoesNotExist:
        return

    try:
        sync_config = repository_sync.sync_config
    except GithubSyncConfig.DoesNotExist:
        return

    if not sync_config.is_active:
        return

    pr_number = pr_data.get("number")
    review_state = review_data.get("state", "").lower()  # approved, changes_requested, commented

    if review_state not in ("approved", "changes_requested"):
        return

    try:
        pr_record = GithubPullRequest.objects.select_related("issue").get(
            repository_sync=repository_sync, pr_number=pr_number
        )
    except GithubPullRequest.DoesNotExist:
        return

    if not pr_record.triggers_automation or not pr_record.issue:
        return

    new_state = get_jet_state_for_pr_state(sync_config, review_state)
    if new_state:
        issue = pr_record.issue
        issue.state = new_state
        issue.updated_by = repository_sync.actor
        issue.save(update_fields=["state", "updated_by", "updated_at"])

        log_sync(
            repository_sync, "pull_request", str(pr_record.github_pr_id),
            "github_to_jet", "success",
            payload={"action": "review", "review_state": review_state},
        )
