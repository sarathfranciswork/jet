"""Bidirectional comment sync between GitHub and Jet."""
import logging

from celery import shared_task
from django.utils import timezone
from sentry_sdk import capture_exception

from jet.db.models import (
    IssueComment,
    GithubIssueSync,
    GithubCommentSync,
    GithubRepositorySync,
    GithubSyncConfig,
    GithubUserMapping,
)
from jet.utils.integrations.github import GithubAPIClient
from .conflict_resolver import should_skip_sync, log_sync

logger = logging.getLogger(__name__)


def _get_client(repository_sync):
    access_tokens_url = (
        repository_sync.workspace_integration.metadata.get("access_tokens_url", "")
    )
    return GithubAPIClient(access_tokens_url)


def _get_repo_info(repository_sync):
    repo = repository_sync.repository
    return repo.owner, repo.name


# ─── GitHub → Jet ───────────────────────────────────────────────────────────


@shared_task
def sync_github_comment_to_jet(repository_sync_id, comment_data, issue_data, action):
    """
    Sync a GitHub issue_comment event to Jet.

    Args:
        repository_sync_id: UUID of GithubRepositorySync
        comment_data: dict — the comment object from webhook payload
        issue_data: dict — the issue object from webhook payload
        action: str — "created", "edited", "deleted"
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

    if not sync_config.is_active or not sync_config.sync_comments:
        return

    github_issue_id = issue_data.get("id")
    github_comment_id = comment_data.get("id")

    try:
        issue_sync = GithubIssueSync.objects.select_related("issue").get(
            repository_sync=repository_sync, github_issue_id=github_issue_id
        )
    except GithubIssueSync.DoesNotExist:
        return

    if should_skip_sync(repository_sync, "comment", github_comment_id, "github_to_jet"):
        return

    try:
        if action == "created":
            _handle_comment_created(repository_sync, issue_sync, comment_data)
        elif action == "edited":
            _handle_comment_edited(repository_sync, issue_sync, comment_data)
        elif action == "deleted":
            _handle_comment_deleted(repository_sync, issue_sync, comment_data)

        log_sync(
            repository_sync, "comment", github_comment_id, "github_to_jet", "success",
            payload={"action": action},
        )
    except Exception as e:
        logger.exception(f"Error syncing GitHub comment {github_comment_id} to Jet")
        log_sync(
            repository_sync, "comment", github_comment_id, "github_to_jet", "failed",
            error_message=str(e),
        )
        capture_exception(e)


def _handle_comment_created(repository_sync, issue_sync, comment_data):
    """Create a Jet comment from a GitHub comment."""
    github_comment_id = comment_data["id"]

    # Check if already synced
    if GithubCommentSync.objects.filter(
        issue_sync=issue_sync, repo_comment_id=github_comment_id
    ).exists():
        return

    # Try to attribute to mapped user
    commenter_login = comment_data.get("user", {}).get("login", "")
    actor = repository_sync.actor
    try:
        user_mapping = GithubUserMapping.objects.get(
            workspace_id=repository_sync.workspace_id,
            github_username=commenter_login,
        )
        actor = user_mapping.user
    except GithubUserMapping.DoesNotExist:
        pass

    comment_body = comment_data.get("body", "")
    # Prefix with GitHub user attribution if using bot
    if actor == repository_sync.actor and commenter_login:
        comment_body = f"**@{commenter_login}** (via GitHub):\n\n{comment_body}"

    comment = IssueComment.objects.create(
        comment_html=comment_body,
        issue=issue_sync.issue,
        actor=actor,
        project_id=repository_sync.project_id,
        workspace_id=repository_sync.workspace_id,
        created_by=actor,
        updated_by=actor,
    )

    GithubCommentSync.objects.create(
        repo_comment_id=github_comment_id,
        comment=comment,
        issue_sync=issue_sync,
        project_id=repository_sync.project_id,
        workspace_id=repository_sync.workspace_id,
        last_synced_at=timezone.now(),
    )


def _handle_comment_edited(repository_sync, issue_sync, comment_data):
    """Update a Jet comment when its GitHub counterpart is edited."""
    github_comment_id = comment_data["id"]

    try:
        comment_sync = GithubCommentSync.objects.select_related("comment").get(
            issue_sync=issue_sync, repo_comment_id=github_comment_id
        )
    except GithubCommentSync.DoesNotExist:
        return

    comment = comment_sync.comment
    comment.comment_html = comment_data.get("body", comment.comment_html)
    comment.updated_by = repository_sync.actor
    comment.save(update_fields=["comment_html", "updated_by", "updated_at"])
    comment_sync.last_synced_at = timezone.now()
    comment_sync.save(update_fields=["last_synced_at"])


def _handle_comment_deleted(repository_sync, issue_sync, comment_data):
    """Delete a Jet comment when its GitHub counterpart is deleted."""
    github_comment_id = comment_data["id"]

    try:
        comment_sync = GithubCommentSync.objects.select_related("comment").get(
            issue_sync=issue_sync, repo_comment_id=github_comment_id
        )
    except GithubCommentSync.DoesNotExist:
        return

    comment_sync.comment.delete()
    comment_sync.delete()


# ─── Jet → GitHub ───────────────────────────────────────────────────────────


@shared_task
def sync_comment_to_github(comment_id, project_id, workspace_id, action="created"):
    """
    Sync a Jet comment to GitHub.

    Args:
        comment_id: UUID of the IssueComment
        project_id: UUID of the Project
        workspace_id: UUID of the Workspace
        action: str — "created", "edited", "deleted"
    """
    try:
        repo_sync = GithubRepositorySync.objects.select_related(
            "repository", "workspace_integration", "sync_config"
        ).get(project_id=project_id)
    except GithubRepositorySync.DoesNotExist:
        return

    try:
        sync_config = repo_sync.sync_config
    except GithubSyncConfig.DoesNotExist:
        return

    if not sync_config.is_active or not sync_config.sync_comments:
        return
    if sync_config.sync_direction == "github_to_jet":
        return

    try:
        comment = IssueComment.objects.select_related("issue").get(id=comment_id)
    except IssueComment.DoesNotExist:
        return

    try:
        issue_sync = GithubIssueSync.objects.get(
            repository_sync=repo_sync, issue=comment.issue
        )
    except GithubIssueSync.DoesNotExist:
        return

    client = _get_client(repo_sync)
    owner, repo_name = _get_repo_info(repo_sync)

    try:
        if action == "created":
            github_comment = client.create_comment(
                owner, repo_name, issue_sync.github_issue_number,
                body=comment.comment_html or "",
            )
            GithubCommentSync.objects.create(
                repo_comment_id=github_comment["id"],
                comment=comment,
                issue_sync=issue_sync,
                project_id=project_id,
                workspace_id=workspace_id,
                last_synced_at=timezone.now(),
            )
        elif action == "edited":
            try:
                comment_sync = GithubCommentSync.objects.get(
                    issue_sync=issue_sync, comment=comment
                )
                client.update_comment(
                    owner, repo_name, comment_sync.repo_comment_id,
                    body=comment.comment_html or "",
                )
                comment_sync.last_synced_at = timezone.now()
                comment_sync.save(update_fields=["last_synced_at"])
            except GithubCommentSync.DoesNotExist:
                pass
        elif action == "deleted":
            try:
                comment_sync = GithubCommentSync.objects.get(
                    issue_sync=issue_sync, comment=comment
                )
                client.delete_comment(owner, repo_name, comment_sync.repo_comment_id)
                comment_sync.delete()
            except GithubCommentSync.DoesNotExist:
                pass

        log_sync(
            repo_sync, "comment", str(comment_id), "jet_to_github", "success",
            payload={"action": action},
        )
    except Exception as e:
        logger.exception(f"Error syncing Jet comment {comment_id} to GitHub")
        log_sync(
            repo_sync, "comment", str(comment_id), "jet_to_github", "failed",
            error_message=str(e),
        )
        capture_exception(e)
