"""Parse issue references from PR titles, bodies, and commit messages."""
import re

from jet.db.models import Issue


# [WEB-123] — bracket notation triggers automation
BRACKET_REF_PATTERN = re.compile(r"\[([A-Z][A-Z0-9]+-\d+)\]")

# WEB-123 — bare notation (used on text with bracket refs already stripped)
BARE_REF_PATTERN = re.compile(r"\b([A-Z][A-Z0-9]+-\d+)\b")


def parse_issue_references(text):
    """
    Parse issue references from text.

    Returns:
        tuple: (bracket_refs, bare_refs)
            - bracket_refs: list of refs like "WEB-123" from [WEB-123] notation (triggers automation)
            - bare_refs: list of refs like "WEB-123" from bare notation (link-only)
    """
    if not text:
        return [], []

    bracket_refs = BRACKET_REF_PATTERN.findall(text)
    # Strip bracket refs from text before searching for bare refs
    cleaned_text = BRACKET_REF_PATTERN.sub("", text)
    bare_refs = BARE_REF_PATTERN.findall(cleaned_text)

    return bracket_refs, bare_refs


def resolve_issue_reference(ref, workspace_id):
    """
    Resolve an issue reference like "WEB-123" to a Jet Issue.

    Args:
        ref: String like "WEB-123" (project_identifier-sequence_id)
        workspace_id: UUID of the workspace

    Returns:
        Issue instance or None
    """
    try:
        parts = ref.rsplit("-", 1)
        if len(parts) != 2:
            return None
        identifier, sequence_str = parts
        sequence_id = int(sequence_str)

        return Issue.objects.filter(
            workspace_id=workspace_id,
            project__identifier=identifier,
            sequence_id=sequence_id,
        ).select_related("project", "state").first()
    except (ValueError, Issue.DoesNotExist):
        return None
