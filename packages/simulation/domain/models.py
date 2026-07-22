from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SimulatedMetrics(BaseModel):
    """Chá»‰ sá»‘ hiá»‡u nÄƒng Ä‘o lÆ°á»ng giáº£ láº­p (Estimated Latency, CPU, RAM)."""

    estimated_latency_ms: float
    expected_cpu_usage: float
    simulated_memory_mb: float

    model_config = ConfigDict(frozen=True)


class SimulationResult(BaseModel):
    """Káº¿t quáº£ thá»±c thi Dry-Run trong Sandbox áº£o cÃ´ láº­p."""

    passed_tests_count: int
    failed_tests_count: int
    simulated_fitness_score: float
    policy_passed: bool
    metrics: SimulatedMetrics

    model_config = ConfigDict(frozen=True)


class Scenario(BaseModel):
    """Ká»‹ch báº£n mÃ´ phá»ng cháº¡y thá»­ Ä‘á» xuáº¥t thay Ä‘á»•i."""

    id: str
    name: str
    description: str
    target_payload: dict[str, Any]

    model_config = ConfigDict(frozen=True)


class Simulation(BaseModel):
    """Thá»±c thá»ƒ Giáº£ láº­p tá»‘i cao Ä‘iá»u hÃ nh viá»‡c kiá»ƒm thá»­ trÆ°á»›c khi sÃ¡p nháº­p."""

    id: str
    scenario_id: str
    status: str  # "SUCCESS" hoáº·c "FAILED"
    result: SimulationResult
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)

