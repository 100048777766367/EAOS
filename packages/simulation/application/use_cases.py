import uuid
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel

from packages.simulation.domain.models import (
    SimulatedMetrics,
    Simulation,
    SimulationResult,
)
from packages.simulation.domain.ports import SimulationRepository


class SimulationRequest(BaseModel):
    scenario_id: str
    scenario_name: str
    description: str
    target_payload: dict[str, Any]


class RunSimulationUseCase:
    """Service Ä‘iá»u phá»‘i Dry-Run cháº¡y Fitness vÃ  Policy áº£o trÃªn Sandbox."""

    def __init__(self, repo: SimulationRepository) -> None:
        self.repo = repo

    def execute(self, request: SimulationRequest) -> Simulation:
        sim_id = f"SIM-{uuid.uuid4().hex[:6].upper()}"

        target_payload = request.target_payload
        has_version = "__version" in target_payload

        # Giáº£ láº­p Clone Sandbox vÃ  cháº¡y khÃ´ 1000 tests
        passed_tests = 1000 if has_version else 950
        failed_tests = 0 if has_version else 50
        sim_fitness = 1.0 if has_version else 0.95
        policy_passed = has_version

        # Giáº£ láº­p tÃ­nh toÃ¡n hiá»‡u nÄƒng táº£i cá»§a CPU, RAM vÃ  Ä‘á»™ trá»…
        estimated_latency = 120.5 if has_version else 250.0
        expected_cpu = 15.4 if has_version else 45.0
        simulated_mem = 128.0 if has_version else 512.0

        metrics = SimulatedMetrics(
            estimated_latency_ms=estimated_latency,
            expected_cpu_usage=expected_cpu,
            simulated_memory_mb=simulated_mem,
        )

        result = SimulationResult(
            passed_tests_count=passed_tests,
            failed_tests_count=failed_tests,
            simulated_fitness_score=sim_fitness,
            policy_passed=policy_passed,
            metrics=metrics,
        )

        status = "SUCCESS" if policy_passed else "FAILED"

        sim = Simulation(
            id=sim_id,
            scenario_id=request.scenario_id,
            status=status,
            result=result,
            created_at=datetime.now(UTC),
        )

        return self.repo.save(sim)
