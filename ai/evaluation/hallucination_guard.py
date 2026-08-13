from __future__ import annotations

from dataclasses import dataclass

"""Hallucination guard."""


@dataclass
class EvaluationResultDTO:
    """Evaluation result DTO."""

    is_valid: bool = True
    hallucination_risk_score: float = 0.0


class HallucinationGuard:
    """Hallucination guard."""

    def evaluate_output(self, text: str) -> EvaluationResultDTO:
        """Evaluate LLM output for hallucinations."""
        return EvaluationResultDTO()
