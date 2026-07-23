"""Unit test suite for EAOS knowledge store engine."""

from pathlib import Path

from tools.knowledge.knowledge_store import KnowledgeStoreEngine

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_knowledge_store_engine_scans_artifacts() -> None:
    """Verifies that knowledge store engine indexes artifacts across categories."""
    engine = KnowledgeStoreEngine(ROOT_PATH)
    artifacts = engine.scan_knowledge_base()
    assert len(artifacts) >= 4
    categories = [a.category for a in artifacts]
    assert "glossary" in categories
    assert "evidence" in categories
    assert "ontologies" in categories
    assert "axioms" in categories
