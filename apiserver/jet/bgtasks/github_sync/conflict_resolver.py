"""Conflict resolution for bidirectional sync."""
import logging

from django.utils import timezone
from datetime import timedelta

from jet.db.models import GithubSyncLog

logger = logging.getLogger(__name__)

# Debounce window to prevent sync loops
DEBOUNCE_SECONDS = 5


def is_bot_user(actor_id, repository_sync):
    """Check if the actor is the bot user for this integration."""
    return str(actor_id) == str(repository_sync.actor_id)


def should_skip_sync(repository_sync, entity_type, entity_id, direction):
    """
    Check if we should skip this sync operation to prevent loops.

    Uses last-write-wins with a debounce window. If the same entity was
    synced in the opposite direction within DEBOUNCE_SECONDS, skip.
    """
    cutoff = timezone.now() - timedelta(seconds=DEBOUNCE_SECONDS)
    opposite_direction = (
        "jet_to_github" if direction == "github_to_jet" else "github_to_jet"
    )

    recent_opposite_sync = GithubSyncLog.objects.filter(
        repository_sync=repository_sync,
        entity_type=entity_type,
        entity_id=str(entity_id),
        direction=opposite_direction,
        status="success",
        created_at__gte=cutoff,
    ).exists()

    if recent_opposite_sync:
        logger.info(
            f"Skipping {direction} sync for {entity_type}:{entity_id} — "
            f"opposite sync within debounce window"
        )
        return True
    return False


def log_sync(
    repository_sync,
    entity_type,
    entity_id,
    direction,
    status,
    error_message="",
    payload=None,
):
    """Create a sync log entry."""
    return GithubSyncLog.objects.create(
        repository_sync=repository_sync,
        entity_type=entity_type,
        entity_id=str(entity_id),
        direction=direction,
        status=status,
        error_message=error_message,
        payload=payload or {},
        project_id=repository_sync.project_id,
        workspace_id=repository_sync.workspace_id,
    )
