"""Tests for GitHub sync: reference parser, HMAC verification, conflict resolution."""
import hashlib
import hmac
from unittest.mock import patch, MagicMock
from django.test import TestCase

from jet.bgtasks.github_sync.reference_parser import (
    parse_issue_references,
    resolve_issue_reference,
)
from jet.utils.integrations.github import verify_github_webhook_signature


class ReferenceParserTest(TestCase):
    """Test issue reference parsing from PR titles and bodies."""

    def test_bracket_refs_extracted(self):
        text = "Fix login bug [WEB-123] and [WEB-456]"
        bracket_refs, bare_refs = parse_issue_references(text)
        self.assertEqual(bracket_refs, ["WEB-123", "WEB-456"])
        self.assertEqual(bare_refs, [])

    def test_bare_refs_extracted(self):
        text = "Related to WEB-789 and PROJ-42"
        bracket_refs, bare_refs = parse_issue_references(text)
        self.assertEqual(bracket_refs, [])
        self.assertEqual(bare_refs, ["WEB-789", "PROJ-42"])

    def test_mixed_refs(self):
        text = "Fixes [WEB-100] and also relates to WEB-200"
        bracket_refs, bare_refs = parse_issue_references(text)
        self.assertEqual(bracket_refs, ["WEB-100"])
        self.assertEqual(bare_refs, ["WEB-200"])

    def test_bare_refs_from_cleaned_text(self):
        text = "[WEB-100] WEB-100"
        bracket_refs, bare_refs = parse_issue_references(text)
        self.assertEqual(bracket_refs, ["WEB-100"])
        # After bracket ref is stripped, the bare WEB-100 still matches
        self.assertEqual(bare_refs, ["WEB-100"])

    def test_empty_text(self):
        bracket_refs, bare_refs = parse_issue_references("")
        self.assertEqual(bracket_refs, [])
        self.assertEqual(bare_refs, [])

    def test_none_text(self):
        bracket_refs, bare_refs = parse_issue_references(None)
        self.assertEqual(bracket_refs, [])
        self.assertEqual(bare_refs, [])

    def test_no_refs(self):
        text = "Just a regular PR with no issue references"
        bracket_refs, bare_refs = parse_issue_references(text)
        self.assertEqual(bracket_refs, [])
        self.assertEqual(bare_refs, [])

    def test_multiline_text(self):
        text = """Fix bug [WEB-10]

        This PR fixes the login page.
        See also WEB-20 for context.
        """
        bracket_refs, bare_refs = parse_issue_references(text)
        self.assertEqual(bracket_refs, ["WEB-10"])
        self.assertEqual(bare_refs, ["WEB-20"])

    def test_alphanumeric_project_identifiers(self):
        text = "[APP2-55] relates to V2-100"
        bracket_refs, bare_refs = parse_issue_references(text)
        self.assertEqual(bracket_refs, ["APP2-55"])
        self.assertEqual(bare_refs, ["V2-100"])


class HMACVerificationTest(TestCase):
    """Test GitHub webhook signature verification."""

    def test_valid_signature(self):
        secret = "test-secret-key"
        payload = b'{"action": "opened"}'
        signature = "sha256=" + hmac.new(
            secret.encode("utf-8"), msg=payload, digestmod=hashlib.sha256
        ).hexdigest()

        self.assertTrue(
            verify_github_webhook_signature(payload, signature, secret)
        )

    def test_invalid_signature(self):
        secret = "test-secret-key"
        payload = b'{"action": "opened"}'
        self.assertFalse(
            verify_github_webhook_signature(payload, "sha256=invalid", secret)
        )

    def test_empty_signature(self):
        secret = "test-secret-key"
        payload = b'{"action": "opened"}'
        self.assertFalse(
            verify_github_webhook_signature(payload, "", secret)
        )

    def test_missing_signature(self):
        secret = "test-secret-key"
        payload = b'{"action": "opened"}'
        self.assertFalse(
            verify_github_webhook_signature(payload, None, secret)
        )
