"""Initial sync — import existing GitHub issues into Jet when a repo is first connected."""
import logging

from celery import shared_task
from django.utils import timezone
from sentry_sdk import capture_exception

from jet.db.models import (
    Issue,
    IssueLabel,
    IssueSequence,
    Label,
    GithubIssueSync,
    GithubRepositorySync,
    GithubSyncConfig,
    State,
)
from jet.utils.integrations.github import GithubAPIClient
from .conflict_resolver import log_sync

logger = logging.getLogger(__name__)


@shared_task
def initial_github_sync(repository_sync_id):
    """
    Import all open issues from a GitHub repo that have the trigger label.
    Called when a repo is first connected to a project.
    """
    try:
        repo_sync = GithubRepositorySync.objects.select_related(
            "repository", "workspace_integration"
        ).get(id=repository_sync_id)
    except GithubRepositorySync.DoesNotExist:
        logger.error(f"GithubRepositorySync {repository_sync_id} not found")
        return

    # Get or create sync config
    try:
        sync_config = repo_sync.sync_config
    except Exception:
        sync_config = None

    trigger_label = "Jet"
    if sync_config:
        trigger_label = sync_config.github_trigger_label or "Jet"

    access_tokens_url = repo_sync.workspace_integration.metadata.get(
        "access_tokens_url", ""
    )
    if not access_tokens_url:
        logger.error(f"No access_tokens_url for repo_sync {repository_sync_id}")
        return

    client = GithubAPIClient(access_tokens_url)
    owner = repo_sync.repository.owner
    repo_name = repo_sync.repository.name

    # Get default state for the project
    default_state = State.objects.filter(
        project_id=repo_sync.project_id,
        workspace_id=repo_sync.workspace_id,
    ).order_by("sequence").first()

    # Get the sync label
    sync_label = repo_sync.label

    # Fetch all open issues (paginated)
    page = 1
    imported_count = 0

    while True:
        try:
            issues = client._request(
                "GET",
                f"/repos/{owner}/{repo_name}/issues",
                params={
                    "state": "open",
                    "per_page": 100,
                    "page": page,
                    "sort": "created",
                    "direction": "asc",
                },
            )
        except Exception as e:
            logger.exception(f"Error fetching issues page {page}")
            break

        if not issues:
            break

        for gh_issue in issues:
            # Skip pull requests (GitHub API includes PRs in issues endpoint)
            if gh_issue.get("pull_request"):
                continue

            github_issue_id = gh_issue["id"]
            github_issue_number = gh_issue["number"]

            # Check if already synced
            if GithubIssueSync.objects.filter(
                repository_sync=repo_sync, github_issue_id=github_issue_id
            ).exists():
                continue

            # Check if issue has trigger label (import all if no specific label filter)
            gh_labels = [l.get("name", "").lower() for l in gh_issue.get("labels", [])]
            has_trigger = trigger_label.lower() in gh_labels

            # Import all issues (not just labeled ones) for initial sync
            # This gives the user a full picture of their repo

            # Get next sequence ID
            last_seq = IssueSequence.objects.filter(
                project_id=repo_sync.project_id
            ).order_by("-sequence").first()
            next_sequence = (last_seq.sequence + 1) if last_seq else 1

            try:
                issue = Issue.objects.create(
                    name=gh_issue.get("title", ""),
                    description_html=gh_issue.get("body") or "",
                    project_id=repo_sync.project_id,
                    workspace_id=repo_sync.workspace_id,
                    state=default_state,
                    sequence_id=next_sequence,
                    created_by=repo_sync.actor,
                    updated_by=repo_sync.actor,
                )

                IssueSequence.objects.create(
                    issue=issue,
                    sequence=next_sequence,
                    project_id=repo_sync.project_id,
                    workspace_id=repo_sync.workspace_id,
                )

                # Add sync label
                if sync_label:
                    IssueLabel.objects.get_or_create(
                        issue=issue,
                        label=sync_label,
                        project_id=repo_sync.project_id,
                        workspace_id=repo_sync.workspace_id,
                    )

                # Sync GitHub labels to Jet
                for gh_label in gh_issue.get("labels", []):
                    label_name = gh_label.get("name", "")
                    label_color = "#" + gh_label.get("color", "000000")
                    label, _ = Label.objects.get_or_create(
                        name=label_name,
                        project_id=repo_sync.project_id,
                        defaults={
                            "color": label_color,
                            "workspace_id": repo_sync.workspace_id,
                        },
                    )
                    IssueLabel.objects.get_or_create(
                        issue=issue,
                        label=label,
                        project_id=repo_sync.project_id,
                        workspace_id=repo_sync.workspace_id,
                    )

                # Create sync record
                GithubIssueSync.objects.create(
                    repo_issue_id=github_issue_id,
                    github_issue_id=github_issue_id,
                    github_issue_number=github_issue_number,
                    issue=issue,
                    issue_url=gh_issue.get("html_url", ""),
                    repository_sync=repo_sync,
                    project_id=repo_sync.project_id,
                    workspace_id=repo_sync.workspace_id,
                    last_synced_at=timezone.now(),
                )

                imported_count += 1
                logger.info(
                    f"Imported GitHub issue #{github_issue_number}: {gh_issue.get('title', '')}"
                )

            except Exception as e:
                logger.exception(
                    f"Error importing GitHub issue #{github_issue_number}"
                )
                capture_exception(e)
                continue

        # Next page
        if len(issues) < 100:
            break
        page += 1

    logger.info(
        f"Initial sync complete for {owner}/{repo_name}: imported {imported_count} issues"
    )

    if imported_count > 0:
        log_sync(
            repo_sync, "issue", "initial_sync", "github_to_jet", "success",
            payload={"imported_count": imported_count},
        )
