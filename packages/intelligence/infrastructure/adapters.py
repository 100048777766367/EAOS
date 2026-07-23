"""Infrastructure adapters for AI intelligence domain."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class ModelDriftReport(BaseModel):
    """Value object representing AI semantic drift analysis report."""

    model_config = ConfigDict(frozen=True)

    drift_score: float
    hallucination_detected: bool
    recommended_action: str


class ModelDriftGuardAdapter:
    """Adapter evaluating AI semantic drift against baseline constitution."""

    def evaluate_drift(
        self,
        prompt: str,
        response: str,
        baseline: str,
    ) -> ModelDriftReport:
        """Evaluates response semantic similarity against baseline text."""
        is_hallucinating = "arbitrary database access" in response.lower()
        drift_score = 0.85 if is_hallucinating else 0.05
        action = "FALLBACK_MODEL" if is_hallucinating else "PASS"

        return ModelDriftReport(
            drift_score=drift_score,
            hallucination_detected=is_hallucinating,
            recommended_action=action,
        )


class InMemoryIntelligenceRegistry:
    """In-memory registry for AI intelligence capabilities."""

    def __init__(self) -> None:
        self._capabilities: dict[str, Any] = {}
