"""Quality fitness function verifying zero linter and MyPy errors."""

from pydantic import BaseModel, ConfigDict


class QualityFitnessScoreDTO(BaseModel):
    """Value object representing code quality fitness metrics."""

    model_config = ConfigDict(frozen=True)

    dimension: str
    passed: bool
    mypy_errors: int
    ruff_errors: int


class QualityFitnessEvaluator:
    """Evaluator testing static code quality and line length limits."""

    def evaluate_quality_fitness(
        self,
        mypy_errors: int = 0,
        ruff_errors: int = 0,
    ) -> QualityFitnessScoreDTO:
        """Evaluates code quality reports."""
        passed = mypy_errors == 0 and ruff_errors == 0

        return QualityFitnessScoreDTO(
            dimension="QUALITY_FITNESS",
            passed=passed,
            mypy_errors=mypy_errors,
            ruff_errors=ruff_errors,
        )
