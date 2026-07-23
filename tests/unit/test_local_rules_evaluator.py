"""Unit test suite for EAOS local operational rules engine."""

from pathlib import Path

from packages.policy_engine.infrastructure.rules_evaluator import (
    LocalRulesEvaluatorEngine,
)

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_local_rules_evaluator_discovers_all_8_categories() -> None:
    """Verifies rule engine discovers rule files across all 8 categories."""
    engine = LocalRulesEvaluatorEngine(ROOT_PATH)
    rules = engine.discover_rules()
    assert len(rules) >= 8
    categories = {r.category for r in rules}
    assert "ai" in categories
    assert "architecture" in categories
    assert "business" in categories
    assert "compliance" in categories
    assert "engineering" in categories
    assert "quality" in categories
    assert "runtime" in categories
    assert "security" in categories


def test_local_rules_evaluator_executes_evaluation() -> None:
    """Verifies rule evaluation execution across discovered rules."""
    engine = LocalRulesEvaluatorEngine(ROOT_PATH)
    results = engine.evaluate_all({"env": "production"})
    assert len(results) >= 8
    assert all(r.passed for r in results)
