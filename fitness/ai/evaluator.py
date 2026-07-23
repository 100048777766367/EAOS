"""AI fitness function evaluating model drift and token budgets."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class AIFitnessScoreDTO(BaseModel):
    """Value object representing AI fitness evaluation results."""

    model_config = ConfigDict(frozen=True)

    dimension: str
    passed: bool
    drift_score: float
    cost_within_budget: bool


class AIFitnessEvaluator:
    """Evaluator testing AI model drift and FinOps cost boundaries."""

    def evaluate_ai_fitness(
        self,
        telemetry: dict[str, Any],
    ) -> AIFitnessScoreDTO:
        """Evaluates AI interaction metrics against constitutional bounds."""
        drift = float(telemetry.get("drift_score", 0.05))
        cost = float(telemetry.get("estimated_cost_usd", 0.001))

        passed = drift < 0.20 and cost <= 0.05

        return AIFitnessScoreDTO(
            dimension="AI_FITNESS",
            passed=passed,
            drift_score=drift,
            cost_within_budget=cost <= 0.05,
        )
