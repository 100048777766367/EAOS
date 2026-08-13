from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

"""Domain Models for Simulation Engine."""


class BranchEnvironmentType(StrEnum):
    """Type of digital twin branch."""

    BASELINE_ALPHA = "BASELINE_ALPHA"
    EXPERIMENTAL_BETA = "EXPERIMENTAL_BETA"


class EmpiricalMetric(BaseModel):
    """Quantitative empirical measurement metric."""

    model_config = ConfigDict(frozen=True)

    metric_name: str = Field(..., description="Name of the metric")
    value: float = Field(..., description="Measured numerical value")
    unit: str = Field(default="ms", description="Unit of measurement")


class EmpiricalEvidence(BaseModel):
    """Evidence record gathered during twin workload execution."""

    model_config = ConfigDict(frozen=True)

    branch_type: BranchEnvironmentType
    branch_id: str
    execution_time_ms: float
    fitness_score: float
    memory_usage_mb: float
    error_count: int
    custom_metrics: list[EmpiricalMetric] = Field(default_factory=list)


class MetricDelta(BaseModel):
    """Calculated difference between Baseline Alpha and Experimental Beta."""

    model_config = ConfigDict(frozen=True)

    metric_name: str
    alpha_value: float
    beta_value: float
    delta_absolute: float
    delta_percentage: float
    is_improvement: bool


class ComparativeResearchReport(BaseModel):
    """Final empirical research report comparing twin branches."""

    model_config = ConfigDict(frozen=True)

    report_id: str
    experiment_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    alpha_evidence: EmpiricalEvidence
    beta_evidence: EmpiricalEvidence
    deltas: list[MetricDelta]
    overall_recommendation: str
    fitness_delta_pct: float


class Simulation(BaseModel):
    """Thực thể Mô phỏng Giả lập."""

    id: str = Field(default="")
    status: str = Field(default="COMPLETED")
    result: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True)
