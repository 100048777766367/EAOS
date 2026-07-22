"""DTOs for Continuous Improvement application layer."""

from packages.continuous_improvement.domain.models import (
    ImprovementCategory,
    InitiativeStatus,
)
from pydantic import BaseModel


class ActionItemDTO(BaseModel):
    item_id: str
    target_component: str
    description: str
    estimated_risk_score: float


class ImprovementInitiativeDTO(BaseModel):
    initiative_id: str
    title: str
    category: ImprovementCategory
    target_component: str
    roi_score: float
    status: InitiativeStatus
    baseline_value: float
    target_value: float
    achieved_value: float | None = None


class IdentifyOpportunitiesCommand(BaseModel):
    target_component: str
    health_score: float
    drift_index: float
    latency_ms: float


class VerifyInitiativeCommand(BaseModel):
    initiative_id: str
    current_metric_value: float
