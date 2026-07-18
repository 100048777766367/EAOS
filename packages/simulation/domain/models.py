from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SimulatedMetrics(BaseModel):
    """Chỉ số hiệu năng đo lường giả lập (Estimated Latency, CPU, RAM)."""

    estimated_latency_ms: float
    expected_cpu_usage: float
    simulated_memory_mb: float

    model_config = ConfigDict(frozen=True)


class SimulationResult(BaseModel):
    """Kết quả thực thi Dry-Run trong Sandbox ảo cô lập."""

    passed_tests_count: int
    failed_tests_count: int
    simulated_fitness_score: float
    policy_passed: bool
    metrics: SimulatedMetrics

    model_config = ConfigDict(frozen=True)


class Scenario(BaseModel):
    """Kịch bản mô phỏng chạy thử đề xuất thay đổi."""

    id: str
    name: str
    description: str
    target_payload: dict[str, Any]

    model_config = ConfigDict(frozen=True)


class Simulation(BaseModel):
    """Thực thể Giả lập tối cao điều hành việc kiểm thử trước khi sáp nhập."""

    id: str
    scenario_id: str
    status: str  # "SUCCESS" hoặc "FAILED"
    result: SimulationResult
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)