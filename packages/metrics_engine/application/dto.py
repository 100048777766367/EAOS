"""Data Transfer Objects for Metrics Engine application layer."""

from pydantic import BaseModel, Field

from packages.metrics_engine.domain.models import MetricType


class RecordObservationCommand(BaseModel):
    system_id: str = Field(default="EAOS-CORE")
    observation_id: str
    metric_type: MetricType
    value: float
    target_component: str


class CapabilityHealthDTO(BaseModel):
    capability_id: str
    health_score: float
    active_violations: int
    active_incidents: int
    drift_index: float
    status: str


class ArchitectureHealthDashboardDTO(BaseModel):
    system_id: str
    overall_health_score: float
    mttr_minutes: float
    ai_success_rate_percentage: float
    architecture_drift_index: float
    capability_health_list: list[CapabilityHealthDTO]
    computed_at: str
