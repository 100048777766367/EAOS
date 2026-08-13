from pydantic import BaseModel, ConfigDict

"""Architectural Fitness Function Engine for EAOS Governance."""


class FitnessEvaluationResult(BaseModel):
    """Value object representing an architectural fitness evaluation."""

    model_config = ConfigDict(frozen=True)

    rule_name: str
    passed: bool
    penalty_weight: float
    violations_count: int
    details: list[str]


class FitnessFunctionEngine:
    """Evaluates architectural fitness functions across codebase."""

    def evaluate_hexagonal_boundary(self, import_records: list[tuple[str, str]]) -> FitnessEvaluationResult:
        """Verifies Hexagonal Architecture boundary rules."""
        violations: list[str] = []
        for file_path, imported_module in import_records:
            if "domain" in file_path and ("infrastructure" in imported_module or "fastapi" in imported_module):
                violations.append(f"{file_path} -> {imported_module}")

        return FitnessEvaluationResult(
            rule_name="HexagonalBoundaryFitness",
            passed=len(violations) == 0,
            penalty_weight=10.0,
            violations_count=len(violations),
            details=violations,
        )


class GovernancePolicyEngine:
    """Calculates weighted health score dynamically based on policy weights."""

    def calculate_health_score(self, fitness_results: list[FitnessEvaluationResult], empty_dirs_count: int) -> float:
        """Calculates dynamic score from fitness rule evaluation results."""
        total_penalty = sum(res.violations_count * res.penalty_weight for res in fitness_results)
        total_penalty += empty_dirs_count * 2.0
        return max(0.0, 100.0 - total_penalty)
