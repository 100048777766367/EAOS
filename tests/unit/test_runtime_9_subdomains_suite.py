"""Unit test suite for EAOS runtime 9-subdomain manager."""

from pathlib import Path

from platform_services.runtime.runtime_manager import (
    RuntimeManagerEngine,
)

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_runtime_manager_inspects_all_9_subdirectories() -> None:
    """Verifies runtime manager inspects all 9 operational domains."""
    engine = RuntimeManagerEngine(ROOT_PATH)
    summaries = engine.inspect_runtime_health()
    assert len(summaries) == 9
    dir_names = {s.directory_name for s in summaries}
    assert "cache" in dir_names
    assert "policies" in dir_names
    assert "sessions" in dir_names
    assert "state" in dir_names
    assert all(s.status == "ACTIVE" for s in summaries)
