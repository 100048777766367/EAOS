"""Unified fitness functions runner evaluating 6-dimensional scorecard."""

from fitness.ai.evaluator import AIFitnessEvaluator
from fitness.architecture.evaluator import ArchitectureFitnessEvaluator
from fitness.governance.evaluator import GovernanceFitnessEvaluator
from fitness.performance.evaluator import PerformanceFitnessEvaluator
from fitness.quality.evaluator import QualityFitnessEvaluator
from fitness.security.evaluator import SecurityFitnessEvaluator
from pydantic import BaseModel, ConfigDict


class ArchitecturalFitnessScorecardDTO(BaseModel):
    """Value object representing total 6-dimensional fitness scorecard."""

    model_config = ConfigDict(frozen=True)

    overall_score: float
    passed: bool
    ai_passed: bool
    architecture_passed: bool
    governance_passed: bool
    performance_passed: bool
    quality_passed: bool
    security_passed: bool


class ArchitecturalFitnessRunner:
    """Orchestrator running all 6 architectural fitness evaluators."""

    def run_all_fitness_checks(
        self,
    ) -> ArchitecturalFitnessScorecardDTO:
        """Executes 6-dimensional fitness evaluations."""
        ai_res = AIFitnessEvaluator().evaluate_ai_fitness({})
        arch_res = ArchitectureFitnessEvaluator().evaluate_layer_fitness({})
        gov_res = GovernanceFitnessEvaluator().evaluate_governance_fitness()
        perf_res = PerformanceFitnessEvaluator().evaluate_performance_fitness()
        qual_res = QualityFitnessEvaluator().evaluate_quality_fitness()
        sec_res = SecurityFitnessEvaluator().evaluate_security_fitness()

        all_passed = (
            ai_res.passed
            and arch_res.passed
            and gov_res.passed
            and perf_res.passed
            and qual_res.passed
            and sec_res.passed
        )

        return ArchitecturalFitnessScorecardDTO(
            overall_score=100.0 if all_passed else 0.0,
            passed=all_passed,
            ai_passed=ai_res.passed,
            architecture_passed=arch_res.passed,
            governance_passed=gov_res.passed,
            performance_passed=perf_res.passed,
            quality_passed=qual_res.passed,
            security_passed=sec_res.passed,
        )
