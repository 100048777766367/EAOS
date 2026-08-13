"""Unit tests for AI/ capability package."""

from __future__ import annotations

from ai.evaluation.hallucination_guard import HallucinationGuard
from ai.models.model_provider import AIProviderType
from ai.planner.task_decomposer import AITaskDecomposer
from ai.router.model_router import FinOpsModelRouter


def test_finops_model_router() -> None:
    """Test FinOps model router decision."""
    router = FinOpsModelRouter()
    decision = router.route_task(task_complexity="medium")
    assert decision.selected_provider in (
        AIProviderType.GROQ,
        AIProviderType.GEMINI,
    )


def test_ai_task_decomposer() -> None:
    """Test AI task decomposer subtask generation."""
    decomposer = AITaskDecomposer()
    plan = decomposer.decompose("Implement Auth")
    assert len(plan.subtasks) == 3
    assert "architect" in plan.assigned_agents


def test_hallucination_guard() -> None:
    """Test hallucination guard evaluation."""
    guard = HallucinationGuard()
    res = guard.evaluate_output("Valid response text")
    assert res.is_valid is True
    assert res.hallucination_risk_score == 0.0
