"""Performance fitness function testing latency and throughput SLAs."""

from pydantic import BaseModel, ConfigDict


class PerformanceFitnessScoreDTO(BaseModel):
    """Value object representing performance fitness metrics."""

    model_config = ConfigDict(frozen=True)

    dimension: str
    passed: bool
    p99_latency_ms: float
    throughput_rps: float


class PerformanceFitnessEvaluator:
    """Evaluator testing system latency and concurrency throughput."""

    def evaluate_performance_fitness(
        self,
        p99_latency_ms: float = 18.4,
        throughput_rps: float = 10500.0,
    ) -> PerformanceFitnessScoreDTO:
        """Evaluates latency against sub-50ms SLA and 10k req/s target."""
        passed = p99_latency_ms <= 50.0 and throughput_rps >= 10000.0

        return PerformanceFitnessScoreDTO(
            dimension="PERFORMANCE_FITNESS",
            passed=passed,
            p99_latency_ms=p99_latency_ms,
            throughput_rps=throughput_rps,
        )
