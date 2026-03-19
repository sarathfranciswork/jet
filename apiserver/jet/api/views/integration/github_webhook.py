"""GitHub webhook endpoint — receives events from GitHub and dispatches to Celery tasks."""
import json
import logging

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from sentry_sdk import capture_exception

from jet.db.models import GithubRepositorySync, GithubSyncConfig
from jet.utils.integrations.github import verify_github_webhook_signature
from jet.bgtasks.github_sync.webhook_handler import process_github_webhook

logger = logging.getLogger(__name__)


class GithubWebhookEndpoint(APIView):
    """
    Public endpoint for receiving GitHub webhook events.

    Validates HMAC-SHA256 signature, identifies the repository sync,
    and enqueues a Celery task for processing.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        # Get signature and event type from headers
        signature = request.META.get("HTTP_X_HUB_SIGNATURE_256", "")
        event_type = request.META.get("HTTP_X_GITHUB_EVENT", "")
        delivery_id = request.META.get("HTTP_X_GITHUB_DELIVERY", "")

        if not event_type:
            return Response(
                {"error": "Missing X-GitHub-Event header"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Handle ping events early
        if event_type == "ping":
            return Response({"message": "pong"}, status=status.HTTP_200_OK)

        # Parse payload
        try:
            payload = request.data
            if isinstance(payload, str):
                payload = json.loads(payload)
        except (json.JSONDecodeError, Exception) as e:
            return Response(
                {"error": "Invalid JSON payload"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Identify the repository from the payload
        repository_data = payload.get("repository", {})
        repo_id = repository_data.get("id")
        repo_full_name = repository_data.get("full_name", "")

        if not repo_id:
            return Response(
                {"error": "Missing repository data in payload"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Find the matching repository sync
        try:
            repository_sync = GithubRepositorySync.objects.select_related(
                "repository", "sync_config"
            ).get(repository__repository_id=repo_id)
        except GithubRepositorySync.DoesNotExist:
            logger.warning(
                f"No repository sync found for GitHub repo {repo_full_name} (id={repo_id})"
            )
            return Response(
                {"error": "Repository not configured for sync"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except GithubRepositorySync.MultipleObjectsReturned:
            # Multiple projects syncing same repo — process for all
            repo_syncs = GithubRepositorySync.objects.filter(
                repository__repository_id=repo_id
            )
            for repo_sync in repo_syncs:
                self._process_for_repo_sync(
                    repo_sync, signature, event_type, payload, request
                )
            return Response({"message": "accepted"}, status=status.HTTP_200_OK)

        result = self._process_for_repo_sync(
            repository_sync, signature, event_type, payload, request
        )
        if result is not None:
            return result

        return Response({"message": "accepted"}, status=status.HTTP_200_OK)

    def _process_for_repo_sync(
        self, repository_sync, signature, event_type, payload, request
    ):
        """Validate signature and enqueue processing for one repo sync."""
        # Verify webhook signature if config has a secret
        try:
            sync_config = repository_sync.sync_config
            webhook_secret = sync_config.webhook_secret
        except GithubSyncConfig.DoesNotExist:
            webhook_secret = ""

        if webhook_secret and signature:
            raw_body = request.body
            if not verify_github_webhook_signature(raw_body, signature, webhook_secret):
                logger.warning(
                    f"Invalid webhook signature for repo_sync {repository_sync.id}"
                )
                return Response(
                    {"error": "Invalid signature"},
                    status=status.HTTP_403_FORBIDDEN,
                )

        # Enqueue for async processing
        process_github_webhook.delay(
            str(repository_sync.id), event_type, payload
        )
        return None
