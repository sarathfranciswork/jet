"""GitHub webhook event dispatcher."""
import logging

from celery import shared_task
from sentry_sdk import capture_exception

from jet.db.models import GithubRepositorySync

logger = logging.getLogger(__name__)


@shared_task
def process_github_webhook(repository_sync_id, event_type, payload):
    """
    Process a GitHub webhook event by dispatching to the appropriate handler.

    Args:
        repository_sync_id: UUID of the GithubRepositorySync
        event_type: str — the X-GitHub-Event header value
        payload: dict — the webhook payload
    """
    try:
        if event_type == "issues":
            _dispatch_issue_event(repository_sync_id, payload)
        elif event_type == "issue_comment":
            _dispatch_comment_event(repository_sync_id, payload)
        elif event_type == "pull_request":
            _dispatch_pr_event(repository_sync_id, payload)
        elif event_type == "pull_request_review":
            _dispatch_pr_review_event(repository_sync_id, payload)
        elif event_type == "label":
            _dispatch_label_event(repository_sync_id, payload)
        elif event_type == "ping":
            logger.info(f"Received ping webhook for repo_sync {repository_sync_id}")
        else:
            logger.info(f"Unhandled webhook event type: {event_type}")
    except Exception as e:
        logger.exception(f"Error processing webhook {event_type}")
        capture_exception(e)


def _dispatch_issue_event(repository_sync_id, payload):
    from .issue_sync import sync_github_issue_to_jet

    action = payload.get("action", "")
    issue_data = payload.get("issue", {})

    # For labeled/unlabeled events, include the label data in the issue
    if action in ("labeled", "unlabeled"):
        issue_data["label"] = payload.get("label", {})

    supported_actions = (
        "opened", "edited", "closed", "reopened",
        "labeled", "unlabeled", "assigned", "unassigned",
    )
    if action in supported_actions:
        sync_github_issue_to_jet.delay(repository_sync_id, issue_data, action)


def _dispatch_comment_event(repository_sync_id, payload):
    from .comment_sync import sync_github_comment_to_jet

    action = payload.get("action", "")
    comment_data = payload.get("comment", {})
    issue_data = payload.get("issue", {})

    if action in ("created", "edited", "deleted"):
        sync_github_comment_to_jet.delay(
            repository_sync_id, comment_data, issue_data, action
        )


def _dispatch_pr_event(repository_sync_id, payload):
    from .pr_handler import handle_pull_request_event

    action = payload.get("action", "")
    pr_data = payload.get("pull_request", {})

    supported_actions = (
        "opened", "closed", "reopened",
        "converted_to_draft", "ready_for_review",
    )
    if action in supported_actions:
        handle_pull_request_event.delay(repository_sync_id, pr_data, action)


def _dispatch_pr_review_event(repository_sync_id, payload):
    from .pr_handler import handle_pull_request_review_event

    action = payload.get("action", "")
    review_data = payload.get("review", {})
    pr_data = payload.get("pull_request", {})

    if action == "submitted":
        handle_pull_request_review_event.delay(
            repository_sync_id, review_data, pr_data
        )


def _dispatch_label_event(repository_sync_id, payload):
    from .label_sync import sync_github_label_event

    action = payload.get("action", "")
    label_data = payload.get("label", {})

    if action in ("created", "edited", "deleted"):
        sync_github_label_event.delay(repository_sync_id, label_data, action)
