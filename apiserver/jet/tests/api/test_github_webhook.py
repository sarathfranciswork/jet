"""Tests for GitHub webhook endpoint."""
import hashlib
import hmac
import json
import uuid
from unittest.mock import patch

from django.test import TestCase, override_settings
from rest_framework.test import APIClient


class GithubWebhookEndpointTest(TestCase):
    """Integration tests for the webhook endpoint."""

    def setUp(self):
        self.client = APIClient()
        self.webhook_url = "/api/webhooks/github/"

    def test_ping_event_returns_pong(self):
        response = self.client.post(
            self.webhook_url,
            data=json.dumps({"zen": "test"}),
            content_type="application/json",
            HTTP_X_GITHUB_EVENT="ping",
            HTTP_X_GITHUB_DELIVERY=str(uuid.uuid4()),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "pong")

    def test_missing_event_header_returns_400(self):
        response = self.client.post(
            self.webhook_url,
            data=json.dumps({"action": "opened"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_missing_repository_returns_400(self):
        response = self.client.post(
            self.webhook_url,
            data=json.dumps({"action": "opened"}),
            content_type="application/json",
            HTTP_X_GITHUB_EVENT="issues",
            HTTP_X_GITHUB_DELIVERY=str(uuid.uuid4()),
        )
        self.assertEqual(response.status_code, 400)

    def test_unknown_repo_returns_404(self):
        response = self.client.post(
            self.webhook_url,
            data=json.dumps({
                "action": "opened",
                "repository": {"id": 999999, "full_name": "unknown/repo"},
                "issue": {"id": 1, "number": 1},
            }),
            content_type="application/json",
            HTTP_X_GITHUB_EVENT="issues",
            HTTP_X_GITHUB_DELIVERY=str(uuid.uuid4()),
        )
        self.assertEqual(response.status_code, 404)
