"""Tests for PR automation — reference parsing and state mapping."""
from django.test import TestCase

from jet.bgtasks.github_sync.reference_parser import parse_issue_references


class PRReferenceParsingTest(TestCase):
    """Test PR title/body reference parsing for automation triggers."""

    def test_bracket_ref_triggers_automation(self):
        """[WEB-123] in PR title should trigger state automation."""
        title = "[WEB-123] Fix authentication flow"
        bracket_refs, bare_refs = parse_issue_references(title)
        self.assertIn("WEB-123", bracket_refs)
        self.assertEqual(len(bare_refs), 0)

    def test_bare_ref_creates_link_only(self):
        """WEB-123 without brackets should only create a link."""
        title = "Fix authentication flow WEB-123"
        bracket_refs, bare_refs = parse_issue_references(title)
        self.assertEqual(len(bracket_refs), 0)
        self.assertIn("WEB-123", bare_refs)

    def test_multiple_bracket_refs(self):
        """Multiple bracket refs in title and body."""
        text = "[WEB-1] [WEB-2] Fix multiple issues\n\nAlso fixes [WEB-3]"
        bracket_refs, bare_refs = parse_issue_references(text)
        self.assertEqual(set(bracket_refs), {"WEB-1", "WEB-2", "WEB-3"})

    def test_pr_body_with_mixed_refs(self):
        """PR body with both bracket and bare refs."""
        text = """[WEB-100] Implement feature

        This PR implements the feature described in WEB-100.
        Related issues: WEB-200, WEB-300
        Closes [WEB-400]
        """
        bracket_refs, bare_refs = parse_issue_references(text)
        self.assertIn("WEB-100", bracket_refs)
        self.assertIn("WEB-400", bracket_refs)
        self.assertIn("WEB-200", bare_refs)
        self.assertIn("WEB-300", bare_refs)

    def test_no_false_positives(self):
        """Normal text should not produce false references."""
        text = "Update README and fix typos"
        bracket_refs, bare_refs = parse_issue_references(text)
        self.assertEqual(len(bracket_refs), 0)
        self.assertEqual(len(bare_refs), 0)

    def test_case_sensitivity(self):
        """References should be case-sensitive (uppercase only)."""
        text = "[web-123] web-456"
        bracket_refs, bare_refs = parse_issue_references(text)
        # lowercase identifiers should not match
        self.assertEqual(len(bracket_refs), 0)
        self.assertEqual(len(bare_refs), 0)
