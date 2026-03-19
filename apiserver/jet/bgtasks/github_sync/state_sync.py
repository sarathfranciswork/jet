"""State mapping logic for GitHub ↔ Jet state synchronization."""
import logging

from jet.db.models import State

logger = logging.getLogger(__name__)


def get_jet_state_for_github_state(sync_config, github_state):
    """
    Map a GitHub issue state (open/closed) to a Jet state using the sync config mapping.

    Returns State instance or None.
    """
    state_mapping = sync_config.state_mapping or {}
    state_id = state_mapping.get(github_state)
    if not state_id:
        return None
    try:
        return State.objects.get(
            id=state_id,
            project_id=sync_config.project_id,
            workspace_id=sync_config.workspace_id,
        )
    except State.DoesNotExist:
        logger.warning(f"Mapped state {state_id} not found for github_state={github_state}")
        return None


def get_jet_state_for_pr_state(sync_config, pr_state):
    """
    Map a PR lifecycle state to a Jet state.

    pr_state: one of "draft", "open", "closed", "merged", "approved", "changes_requested"
    """
    pr_state_mapping = sync_config.pr_state_mapping or {}
    state_id = pr_state_mapping.get(pr_state)
    if not state_id:
        return None
    try:
        return State.objects.get(
            id=state_id,
            project_id=sync_config.project_id,
            workspace_id=sync_config.workspace_id,
        )
    except State.DoesNotExist:
        logger.warning(f"Mapped state {state_id} not found for pr_state={pr_state}")
        return None


def get_github_state_for_jet_state(sync_config, jet_state_id):
    """
    Reverse map: given a Jet state ID, find the corresponding GitHub state.

    Returns "open", "closed", or None.
    """
    state_mapping = sync_config.state_mapping or {}
    jet_state_id_str = str(jet_state_id)
    for github_state, mapped_state_id in state_mapping.items():
        if str(mapped_state_id) == jet_state_id_str:
            return github_state
    return None
