"""Tests for bidirectional sync and loop prevention."""
from datetime import timedelta
from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.utils import timezone

from jet.bgtasks.github_sync.conflict_resolver import (
    should_skip_sync,
    is_bot_user,
    DEBOUNCE_SECONDS,
)


class LoopPreventionTest(TestCase):
    """Test that bidirectional sync doesn't create infinite loops."""

    @patch("jet.bgtasks.github_sync.conflict_resolver.GithubSyncLog")
    def test_skip_when_opposite_sync_within_debounce(self, mock_log_model):
        """Should skip sync when the opposite direction synced within debounce window."""
        mock_repo_sync = MagicMock()
        mock_log_model.objects.filter.return_value.exists.return_value = True

        result = should_skip_sync(
            mock_repo_sync, "issue", "123", "github_to_jet"
        )
        self.assertTrue(result)

        # Verify we checked for the opposite direction
        filter_kwargs = mock_log_model.objects.filter.call_args[1]
        self.assertEqual(filter_kwargs["direction"], "jet_to_github")

    @patch("jet.bgtasks.github_sync.conflict_resolver.GithubSyncLog")
    def test_allow_when_no_recent_opposite_sync(self, mock_log_model):
        """Should allow sync when no recent opposite-direction sync exists."""
        mock_repo_sync = MagicMock()
        mock_log_model.objects.filter.return_value.exists.return_value = False

        result = should_skip_sync(
            mock_repo_sync, "issue", "123", "github_to_jet"
        )
        self.assertFalse(result)

    def test_bot_user_detection(self):
        """Should correctly identify bot users."""
        import uuid

        actor_id = uuid.uuid4()
        mock_repo_sync = MagicMock()
        mock_repo_sync.actor_id = actor_id

        self.assertTrue(is_bot_user(actor_id, mock_repo_sync))
        self.assertFalse(is_bot_user(uuid.uuid4(), mock_repo_sync))

    @patch("jet.bgtasks.github_sync.conflict_resolver.GithubSyncLog")
    def test_debounce_checks_correct_direction(self, mock_log_model):
        """Debounce should check for the opposite sync direction."""
        mock_repo_sync = MagicMock()
        mock_log_model.objects.filter.return_value.exists.return_value = False

        # When we're doing jet_to_github, should check for github_to_jet
        should_skip_sync(mock_repo_sync, "issue", "456", "jet_to_github")
        filter_kwargs = mock_log_model.objects.filter.call_args[1]
        self.assertEqual(filter_kwargs["direction"], "github_to_jet")
