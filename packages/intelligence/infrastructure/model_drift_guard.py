"""AI Model Hallucination and Semantic Drift Guard for EAOS intelligence."""

from pydantic import BaseModel, ConfigDict


class DriftEvaluationResult(BaseModel):
    """Value object representing semantic model drift evaluation result."""

    model_config = ConfigDict(frozen=True)

    model_name: str
    drift_score: float
    hallucination_detected: bool
    recommended_action: str


class ModelDriftGuard:
    """Evaluates semantic drift and hallucination distance against baseline."""

    def __init__(self, model_name: str = "deepseek/deepseek-r1") -> None:
        self.model_name: str = model_name

    def evaluate_response(
        self,
        prompt: str,
        response: str,
        baseline_text: str,
        max_drift_threshold: float = 0.35,
    ) -> DriftEvaluationResult:
        """Calculates Jaccard semantic distance to detect hallucinations."""
        resp_words = set(response.lower().split())
        base_words = set(baseline_text.lower().split())

        intersection = len(resp_words.intersection(base_words))
        union = len(resp_words.union(base_words))

        jaccard_sim = intersection / union if union > 0 else 0.0
        drift_score = round(1.0 - jaccard_sim, 4)

        hallucinated = drift_score > max_drift_threshold
        action = "FALLBACK_MODEL" if hallucinated else "ACCEPT_RESPONSE"

        return DriftEvaluationResult(
            model_name=self.model_name,
            drift_score=drift_score,
            hallucination_detected=hallucinated,
            recommended_action=action,
        )
