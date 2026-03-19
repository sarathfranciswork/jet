"""Label sync between GitHub and Jet."""
import logging

from celery import shared_task
from sentry_sdk import capture_exception

from jet.db.models import (
    Label,
    IssueLabel,
    GithubIssueSync,
    GithubRepositorySync,
    GithubSyncConfig,
)
from .conflict_resolver import log_sync

logger = logging.getLogger(__name__)


@shared_task
def sync_github_label_event(repository_sync_id, label_data, action):
    """
    Handle GitHub label events (created, edited, deleted).

    These are repo-level label events, not issue-level label assignments.
    """
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

    if not sync_config.is_active or not sync_config.sync_labels:
        return

    label_name = label_data.get("name", "")
    label_color = "#" + label_data.get("color", "000000")

    try:
        if action == "created":
            Label.objects.get_or_create(
                name=label_name,
                project_id=repository_sync.project_id,
                defaults={
                    "color": label_color,
                    "workspace_id": repository_sync.workspace_id,
                },
            )
        elif action == "edited":
            changes = label_data.get("changes", {})
            old_name = changes.get("name", {}).get("from", label_name)
            Label.objects.filter(
                name=old_name,
                project_id=repository_sync.project_id,
            ).update(name=label_name, color=label_color)
        elif action == "deleted":
            # Don't delete Jet labels, just log it
            pass

        log_sync(
            repository_sync, "label", label_name, "github_to_jet", "success",
            payload={"action": action},
        )
    except Exception as e:
        logger.exception(f"Error syncing GitHub label event")
        log_sync(
            repository_sync, "label", label_name, "github_to_jet", "failed",
            error_message=str(e),
        )
        capture_exception(e)
