"""Unit test suite for EAOS static asset manager."""

from pathlib import Path

from tools.assets.asset_manager import AssetManager

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_asset_manager_discovery() -> None:
    """Verifies scanning and listing templates in assets/templates/."""
    manager = AssetManager(ROOT_PATH)
    templates = manager.discover_assets("templates")
    assert len(templates) >= 1
    assert any(t.asset_id == "architecture_document_template" for t in templates)


def test_asset_manager_load_template() -> None:
    """Verifies reading text content from markdown template file."""
    manager = AssetManager(ROOT_PATH)
    content = manager.load_template_text("architecture_document_template.md")
    assert "# EAOS Architecture Document Template" in content
