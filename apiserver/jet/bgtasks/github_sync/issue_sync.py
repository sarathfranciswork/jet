"""Bidirectional issue sync between GitHub and Jet."""
import logging

from celery import shared_task
from django.utils import timezone
from sentry_sdk import capture_exception

from jet.db.models import (
    Issue,
    IssueAssignee,
    IssueLabel,
    IssueSequence,
    Label,
    GithubIssueSync,
    GithubRepositorySync,
    GithubSyncConfig,
    GithubUserMapping,
)
from jet.utils.integrations.github import GithubAPIClient
from .conflict_resolver import is_bot_user, should_skip_sync, log_sync
from .state_sync import get_jet_state_for_github_state, get_github_state_for_jet_state

logger = logging.getLogger(__name__)


def _get_client(repository_sync):
    """Create a GithubAPIClient from a repository sync's workspace integration."""
    access_tokens_url = (
        repository_sync.workspace_integration.metadata.get("access_tokens_url", "")
    )
    return GithubAPIClient(access_tokens_url)


def _get_repo_info(repository_sync):
    """Return (owner, repo) tuple from repository sync."""
    repo = repository_sync.repository
    return repo.owner, repo.name


# ─── GitHub → Jet ───────────────────────────────────────────────────────────


@shared_task
def sync_github_issue_to_jet(repository_sync_id, github_issue_data, action):
    """
    Sync a GitHub issue event to Jet.

    Args:
        repository_sync_id: UUID of GithubRepositorySync
        github_issue_data: dict — the GitHub issue payload from webhook
        action: str — one of "opened", "edited", "closed", "reopened", "labeled", "unlabeled",
                       "assigned", "unassigned"
    """
    try:
        repository_sync = GithubRepositorySync.objects.select_related(
            "repository", "workspace_integration", "sync_config"
        ).get(id=repository_sync_id)
    except GithubRepositorySync.DoesNotExist:
        logger.error(f"GithubRepositorySync {repository_sync_id} not found")
        return

    try:
        sync_config = repository_sync.sync_config
    except GithubSyncConfig.DoesNotExist:
        logger.info(f"No sync config for repository_sync {repository_sync_id}")
        return

    if not sync_config.is_active:
        return

    github_issue_number = github_issue_data.get("number")
    github_issue_id = github_issue_data.get("id")

    if should_skip_sync(repository_sync, "issue", github_issue_id, "github_to_jet"):
        return

    try:
        if action == "opened":
            _handle_github_issue_opened(
                repository_sync, sync_config, github_issue_data
            )
        elif action == "edited":
            _handle_github_issue_edited(
                repository_sync, sync_config, github_issue_data
            )
        elif action in ("closed", "reopened"):
            _handle_github_issue_state_change(
                repository_sync, sync_config, github_issue_data, action
            )
        elif action in ("labeled", "unlabeled"):
            _handle_github_issue_label_change(
                repository_sync, sync_config, github_issue_data, action
            )
        elif action in ("assigned", "unassigned"):
            _handle_github_issue_assignee_change(
                repository_sync, sync_config, github_issue_data, action
            )

        log_sync(
            repository_sync, "issue", github_issue_id, "github_to_jet", "success",
            payload={"action": action, "issue_number": github_issue_number},
        )
    except Exception as e:
        logger.exception(f"Error syncing GitHub issue #{github_issue_number} to Jet")
        log_sync(
            repository_sync, "issue", github_issue_id, "github_to_jet", "failed",
            error_message=str(e),
        )
        capture_exception(e)


def _has_trigger_label(github_issue_data, trigger_label_name):
    """Check if the GitHub issue has the trigger label."""
    labels = github_issue_data.get("labels", [])
    return any(
        label.get("name", "").lower() == trigger_label_name.lower()
        for label in labels
    )


def _handle_github_issue_opened(repository_sync, sync_config, github_issue_data):
    """Create a Jet issue when a GitHub issue with the trigger label is opened."""
    if not _has_trigger_label(github_issue_data, sync_config.github_trigger_label):
        return

    github_issue_number = github_issue_data["number"]
    github_issue_id = github_issue_data["id"]

    # Check if already synced
    if GithubIssueSync.objects.filter(
        repository_sync=repository_sync, github_issue_id=github_issue_id
    ).exists():
        return

    # Get the default state for "open"
    state = get_jet_state_for_github_state(sync_config, "open")

    # Get the next sequence ID
    last_seq = IssueSequence.objects.filter(
        project_id=repository_sync.project_id
    ).order_by("-sequence").first()
    next_sequence = (last_seq.sequence + 1) if last_seq else 1

    # Create the Jet issue
    issue = Issue.objects.create(
        name=github_issue_data.get("title", ""),
        description_html=github_issue_data.get("body") or "",
        project_id=repository_sync.project_id,
        workspace_id=repository_sync.workspace_id,
        state=state,
        sequence_id=next_sequence,
        created_by=repository_sync.actor,
        updated_by=repository_sync.actor,
    )

    # Update sequence tracker
    IssueSequence.objects.create(
        issue=issue,
        sequence=next_sequence,
        project_id=repository_sync.project_id,
        workspace_id=repository_sync.workspace_id,
    )

    # Add the sync label to the issue
    if repository_sync.label:
        IssueLabel.objects.get_or_create(
            issue=issue,
            label=repository_sync.label,
            project_id=repository_sync.project_id,
            workspace_id=repository_sync.workspace_id,
        )

    # Create sync record
    GithubIssueSync.objects.create(
        repo_issue_id=github_issue_id,
        github_issue_id=github_issue_id,
        github_issue_number=github_issue_number,
        issue=issue,
        issue_url=github_issue_data.get("html_url", ""),
        repository_sync=repository_sync,
        project_id=repository_sync.project_id,
        workspace_id=repository_sync.workspace_id,
        last_synced_at=timezone.now(),
    )

    logger.info(
        f"Created Jet issue {issue.id} from GitHub issue #{github_issue_number}"
    )


def _handle_github_issue_edited(repository_sync, sync_config, github_issue_data):
    """Update Jet issue when GitHub issue title/body is edited."""
    github_issue_id = github_issue_data["id"]

    try:
        issue_sync = GithubIssueSync.objects.select_related("issue").get(
            repository_sync=repository_sync, github_issue_id=github_issue_id
        )
    except GithubIssueSync.DoesNotExist:
        return

    issue = issue_sync.issue
    issue.name = github_issue_data.get("title", issue.name)
    body = github_issue_data.get("body")
    if body is not None:
        issue.description_html = body
    issue.updated_by = repository_sync.actor
    issue.save(update_fields=["name", "description_html", "updated_by", "updated_at"])
    issue_sync.last_synced_at = timezone.now()
    issue_sync.save(update_fields=["last_synced_at"])


def _handle_github_issue_state_change(
    repository_sync, sync_config, github_issue_data, action
):
    """Update Jet issue state when GitHub issue is closed/reopened."""
    github_issue_id = github_issue_data["id"]

    try:
        issue_sync = GithubIssueSync.objects.select_related("issue").get(
            repository_sync=repository_sync, github_issue_id=github_issue_id
        )
    except GithubIssueSync.DoesNotExist:
        return

    github_state = "closed" if action == "closed" else "open"
    new_state = get_jet_state_for_github_state(sync_config, github_state)
    if new_state:
        issue = issue_sync.issue
        issue.state = new_state
        issue.updated_by = repository_sync.actor
        issue.save(update_fields=["state", "updated_by", "updated_at"])
        issue_sync.last_synced_at = timezone.now()
        issue_sync.save(update_fields=["last_synced_at"])


def _handle_github_issue_label_change(
    repository_sync, sync_config, github_issue_data, action
):
    """Sync label changes from GitHub to Jet."""
    if not sync_config.sync_labels:
        return

    github_issue_id = github_issue_data["id"]

    try:
        issue_sync = GithubIssueSync.objects.select_related("issue").get(
            repository_sync=repository_sync, github_issue_id=github_issue_id
        )
    except GithubIssueSync.DoesNotExist:
        # If it's a "labeled" event with the trigger label, treat as issue creation
        if action == "labeled":
            label_data = github_issue_data.get("label", {})
            if label_data.get("name", "").lower() == sync_config.github_trigger_label.lower():
                _handle_github_issue_opened(repository_sync, sync_config, github_issue_data)
        return

    issue = issue_sync.issue

    # Sync all GitHub labels to Jet
    github_labels = github_issue_data.get("labels", [])
    for gh_label in github_labels:
        label_name = gh_label.get("name", "")
        label_color = "#" + gh_label.get("color", "000000")
        label, _ = Label.objects.get_or_create(
            name=label_name,
            project_id=repository_sync.project_id,
            defaults={
                "color": label_color,
                "workspace_id": repository_sync.workspace_id,
            },
        )
        IssueLabel.objects.get_or_create(
            issue=issue,
            label=label,
            project_id=repository_sync.project_id,
            workspace_id=repository_sync.workspace_id,
        )


def _handle_github_issue_assignee_change(
    repository_sync, sync_config, github_issue_data, action
):
    """Sync assignee changes from GitHub to Jet."""
    if not sync_config.sync_assignees:
        return

    github_issue_id = github_issue_data["id"]

    try:
        issue_sync = GithubIssueSync.objects.select_related("issue").get(
            repository_sync=repository_sync, github_issue_id=github_issue_id
        )
    except GithubIssueSync.DoesNotExist:
        return

    issue = issue_sync.issue
    assignees = github_issue_data.get("assignees", [])

    for assignee in assignees:
        github_username = assignee.get("login", "")
        try:
            user_mapping = GithubUserMapping.objects.get(
                workspace_id=repository_sync.workspace_id,
                github_username=github_username,
            )
            IssueAssignee.objects.get_or_create(
                issue=issue,
                assignee=user_mapping.user,
                project_id=repository_sync.project_id,
                workspace_id=repository_sync.workspace_id,
            )
        except GithubUserMapping.DoesNotExist:
            continue


# ─── Jet → GitHub ───────────────────────────────────────────────────────────


@shared_task
def sync_issue_to_github(issue_id, project_id, workspace_id, field=None):
    """
    Sync a Jet issue change to GitHub.

    Args:
        issue_id: UUID of the Jet Issue
        project_id: UUID of the Project
        workspace_id: UUID of the Workspace
        field: optional str — specific field that changed ("state", "name", "description", "label")
    """
    try:
        repo_sync = GithubRepositorySync.objects.select_related(
            "repository", "workspace_integration", "sync_config"
        ).get(project_id=project_id)
    except GithubRepositorySync.DoesNotExist:
        return
    except GithubRepositorySync.MultipleObjectsReturned:
        repo_sync = GithubRepositorySync.objects.select_related(
            "repository", "workspace_integration", "sync_config"
        ).filter(project_id=project_id).first()

    try:
        sync_config = repo_sync.sync_config
    except GithubSyncConfig.DoesNotExist:
        return

    if not sync_config.is_active or sync_config.sync_direction == "github_to_jet":
        return

    try:
        issue = Issue.objects.select_related("state", "project").get(id=issue_id)
    except Issue.DoesNotExist:
        return

    # Check for sync loop
    try:
        issue_sync = GithubIssueSync.objects.get(
            repository_sync=repo_sync, issue=issue
        )
    except GithubIssueSync.DoesNotExist:
        # Issue not yet synced — check if it should be created on GitHub
        _maybe_create_github_issue(repo_sync, sync_config, issue)
        return

    if should_skip_sync(repo_sync, "issue", issue_sync.github_issue_id, "jet_to_github"):
        return

    client = _get_client(repo_sync)
    owner, repo_name = _get_repo_info(repo_sync)

    try:
        update_kwargs = {}
        if field in (None, "name"):
            update_kwargs["title"] = issue.name
        if field in (None, "description"):
            update_kwargs["body"] = issue.description_html or ""
        if field in (None, "state"):
            github_state = get_github_state_for_jet_state(
                sync_config, issue.state_id
            )
            if github_state:
                update_kwargs["state"] = github_state

        if update_kwargs:
            client.update_issue(
                owner, repo_name, issue_sync.github_issue_number, **update_kwargs
            )
            issue_sync.last_synced_at = timezone.now()
            issue_sync.save(update_fields=["last_synced_at"])
            log_sync(
                repo_sync, "issue", issue_sync.github_issue_id, "jet_to_github", "success",
                payload={"field": field, "issue_number": issue_sync.github_issue_number},
            )
    except Exception as e:
        logger.exception(f"Error syncing Jet issue {issue_id} to GitHub")
        log_sync(
            repo_sync, "issue", issue_sync.github_issue_id, "jet_to_github", "failed",
            error_message=str(e),
        )
        capture_exception(e)


def _maybe_create_github_issue(repo_sync, sync_config, issue):
    """Create a GitHub issue if the Jet issue has the trigger label."""
    if not sync_config.jet_trigger_label:
        return

    # Check if issue has the trigger label
    has_label = IssueLabel.objects.filter(
        issue=issue, label=sync_config.jet_trigger_label
    ).exists()
    if not has_label:
        return

    client = _get_client(repo_sync)
    owner, repo_name = _get_repo_info(repo_sync)

    try:
        # Collect labels
        labels = [sync_config.github_trigger_label]
        issue_labels = Label.objects.filter(
            issue_labels__issue=issue,
            project_id=repo_sync.project_id,
        ).values_list("name", flat=True)
        labels.extend(issue_labels)

        github_issue = client.create_issue(
            owner,
            repo_name,
            title=issue.name,
            body=issue.description_html or "",
            labels=list(set(labels)),
        )

        GithubIssueSync.objects.create(
            repo_issue_id=github_issue["id"],
            github_issue_id=github_issue["id"],
            github_issue_number=github_issue["number"],
            issue=issue,
            issue_url=github_issue.get("html_url", ""),
            repository_sync=repo_sync,
            project_id=repo_sync.project_id,
            workspace_id=repo_sync.workspace_id,
            last_synced_at=timezone.now(),
        )

        log_sync(
            repo_sync, "issue", github_issue["id"], "jet_to_github", "success",
            payload={"action": "created", "issue_number": github_issue["number"]},
        )
        logger.info(
            f"Created GitHub issue #{github_issue['number']} from Jet issue {issue.id}"
        )
    except Exception as e:
        logger.exception(f"Error creating GitHub issue from Jet issue {issue.id}")
        log_sync(
            repo_sync, "issue", str(issue.id), "jet_to_github", "failed",
            error_message=str(e),
        )
        capture_exception(e)
