"""Data Transfer Objects for the Feedback application layer."""

from packages.feedback.domain.models import (
    FeedbackSeverity,
    FeedbackSource,
)
from pydantic import BaseModel, Field


class IngestionSignalCommand(BaseModel):
    signal_id: str = Field(..., description="Unique ID of the signal")
    loop_id: str = Field(..., description="ID of the feedback loop aggregate")
    source: FeedbackSource
    severity: FeedbackSeverity
    metric_name: str
    observed_value: float
    threshold_value: float
    message: str


class FeedbackProcessResult(BaseModel):
    signal_id: str
    is_violation: bool
    adaptation_triggered: bool
    decision_id: str | None = None
    action_type: str | None = None
    requires_approval: bool = False
