"""Unit test suite for EAOS knowledge repository scanner."""

from pathlib import Path

from tools.knowledge.knowledge_repository_scanner import (
    KnowledgeRepositoryScanner,
)

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_knowledge_repository_scanner_indexes_all_17_categories() -> None:
    """Verifies that knowledge repository scanner indexes all 17 categories."""
    scanner = KnowledgeRepositoryScanner(ROOT_PATH)
    categories = scanner.scan_knowledge_base()
    assert len(categories) == 17
    cat_names = [c.category for c in categories]
    assert "adr" in cat_names
    assert "evidence" in cat_names
    assert "glossary" in cat_names
    assert "metamodels" in cat_names
