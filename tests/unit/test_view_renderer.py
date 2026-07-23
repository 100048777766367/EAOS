"""Unit test suite for EAOS view renderer engine."""

from pathlib import Path

from tools.views.view_renderer import ViewRendererEngine

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_view_renderer_discovers_all_5_categories() -> None:
    """Verifies view renderer discovers view configuration definitions."""
    engine = ViewRendererEngine(ROOT_PATH)
    views = engine.discover_views()
    assert len(views) >= 5
    categories = {v.category for v in views}
    assert "eaos" in categories
    assert "foundation" in categories
    assert "library" in categories
    assert "research" in categories
    assert "runtime" in categories


def test_view_renderer_loads_view_json() -> None:
    """Verifies loading JSON view configuration dictionary."""
    engine = ViewRendererEngine(ROOT_PATH)
    data = engine.load_view_json("runtime", "control_room_view.json")
    assert "title" in data
    assert data.get("status") != "NOT_FOUND"
