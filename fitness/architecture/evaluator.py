"""Architecture fitness function enforcing Hexagonal layer isolation."""

from pydantic import BaseModel, ConfigDict


class ArchitectureFitnessScoreDTO(BaseModel):
    """Value object representing structural architecture fitness."""

    model_config = ConfigDict(frozen=True)

    dimension: str
    passed: bool
    boundary_violations: int


class ArchitectureFitnessEvaluator:
    """Evaluator testing layer boundary and dependency direction rules."""

    def evaluate_layer_fitness(
        self,
        dependency_graph: dict[str, set[str]],
    ) -> ArchitectureFitnessScoreDTO:
        """Evaluates dependency graph for domain layer leakage."""
        violations = 0
        for pkg, deps in dependency_graph.items():
            if "domain" in pkg.lower():
                for dep in deps:
                    if "infrastructure" in dep.lower():
                        violations += 1

        return ArchitectureFitnessScoreDTO(
            dimension="ARCHITECTURE_FITNESS",
            passed=violations == 0,
            boundary_violations=violations,
        )
