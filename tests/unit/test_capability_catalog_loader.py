"""Unit test suite for EAOS capability catalog loader."""

from pathlib import Path

from packages.capability.infrastructure.capability_catalog_loader import (
    CapabilityCatalogLoader,
)

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_capability_catalog_loader_scans_manifests() -> None:
    """Verifies that all 9 capability manifests are discovered and parsed."""
    loader = CapabilityCatalogLoader(ROOT_PATH)
    manifests = loader.scan_catalog()
    assert len(manifests) >= 9
    ids = [m.id for m in manifests]
    assert "cap.analytics" in ids
    assert "cap.security" in ids
    assert "cap.workflow" in ids
