"""Unit test suite for EAOS document lifecycle validator."""

from pathlib import Path

from tools.docs.doc_lifecycle_validator import DocumentLifecycleValidator

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_document_lifecycle_validator_audits_core_docs() -> None:
    """Verifies that documentation validator audits mandatory markdown files."""
    validator = DocumentLifecycleValidator(ROOT_PATH)
    audits = validator.audit_core_documentation()
    assert len(audits) == 7
    doc_ids = [a.doc_id for a in audits]
    assert "architecture_constitution" in doc_ids
    assert "engineering_guide" in doc_ids
    assert "roadmap" in doc_ids
    assert all(a.exists for a in audits)
