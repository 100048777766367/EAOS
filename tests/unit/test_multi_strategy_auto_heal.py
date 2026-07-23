"""Unit test suite for multi-strategy auto-healing engine."""

from pathlib import Path

from tools.ops.multi_strategy_auto_heal import (
    MultiStrategyAutoHealEngine,
)


def test_multi_strategy_auto_heal_rollback_and_success(
    tmp_path: Path,
) -> None:
    """Verifies multi-strategy execution, rollback count, and experience log."""
    engine = MultiStrategyAutoHealEngine(tmp_path)
    strategies = [
        {"name": "Strategy 1: Syntax Sanitization", "should_succeed": False},
        {"name": "Strategy 2: Ruff Unsafe Fixes", "should_succeed": True},
    ]
    res = engine.execute_healing_chain("uv run task lint", strategies)

    assert res.status == "RESOLVED"
    assert res.successful_strategy == "Strategy 2: Ruff Unsafe Fixes"
    assert res.rolled_back_attempts == 1
    assert len(res.attempts) == 2
    assert (tmp_path / "knowledge" / "evidence" / "auto_heal_learning.json").exists()
    assert (tmp_path / "docs" / "operations" / "AUTO_HEAL_LOG.md").exists()
