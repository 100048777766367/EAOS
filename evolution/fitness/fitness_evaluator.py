from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Architecture Fitness Functions Evaluator Engine."""


class FitnessEvaluationDTO(BaseModel):
    """Value object representing a fitness function evaluation result."""

    model_config = ConfigDict(frozen=True)

    fitness_score: float = Field(default=100.0, description="Score 0-100")
    total_rules_checked: int = Field(default=0)
    passed_rules_count: int = Field(default=0)
    is_compliant: bool = Field(default=True)


class ArchitectureFitnessEvaluator:
    """Evaluator continuously calculating architectural fitness scores."""

    def evaluate_fitness(self, violations_count: int = 0, total_rules: int = 20) -> FitnessEvaluationDTO:
        """Calculate fitness score based on violations."""
        score = max(0.0, 100.0 - (violations_count * 5.0))
        passed_count = max(0, total_rules - violations_count)

        return FitnessEvaluationDTO(
            fitness_score=score,
            total_rules_checked=total_rules,
            passed_rules_count=passed_count,
            is_compliant=violations_count == 0,
        )
