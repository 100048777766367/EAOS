"""Security fitness function evaluating Zero-Trust and secrets."""

from pydantic import BaseModel, ConfigDict


class SecurityFitnessScoreDTO(BaseModel):
    """Value object representing security fitness evaluation."""

    model_config = ConfigDict(frozen=True)

    dimension: str
    passed: bool
    secrets_detected: int
    post_quantum_active: bool


class SecurityFitnessEvaluator:
    """Evaluator testing security architecture and credential leaks."""

    def evaluate_security_fitness(
        self,
        secrets_detected: int = 0,
        post_quantum_active: bool = True,
    ) -> SecurityFitnessScoreDTO:
        """Evaluates security compliance checks."""
        passed = secrets_detected == 0 and post_quantum_active

        return SecurityFitnessScoreDTO(
            dimension="SECURITY_FITNESS",
            passed=passed,
            secrets_detected=secrets_detected,
            post_quantum_active=post_quantum_active,
        )
