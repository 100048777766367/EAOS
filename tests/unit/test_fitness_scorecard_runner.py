"""Unit test suite for EAOS architectural fitness scorecard runner."""

from tools.fitness.fitness_runner import ArchitecturalFitnessRunner


def test_architectural_fitness_runner_scorecard() -> None:
    """Verifies that the fitness runner evaluates all 6 dimensions."""
    runner = ArchitecturalFitnessRunner()
    scorecard = runner.run_all_fitness_checks()
    assert scorecard.passed is True
    assert scorecard.overall_score == 100.0
    assert scorecard.ai_passed is True
    assert scorecard.architecture_passed is True
    assert scorecard.governance_passed is True
    assert scorecard.performance_passed is True
    assert scorecard.quality_passed is True
    assert scorecard.security_passed is True
