"""Unit test suite for EAOS policy manifest loader."""

from pathlib import Path

from packages.policy_engine.infrastructure.policy_manifest_loader import (
    PolicyManifestLoader,
)

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_policy_manifest_loader_discovers_all_7_categories() -> None:
    """Verifies policy manifest loader discovers YAML files in 7 categories."""
    loader = PolicyManifestLoader(ROOT_PATH)
    policies = loader.discover_policies()
    assert len(policies) >= 7
    categories = {p.category for p in policies}
    assert "ai" in categories
    assert "architecture" in categories
    assert "compliance" in categories
    assert "engineering" in categories
    assert "governance" in categories
    assert "quality" in categories
    assert "security" in categories
