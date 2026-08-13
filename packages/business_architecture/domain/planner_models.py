from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""Enterprise Task Planner Domain Models (Phase 2)."""


class ApprovalMode(StrEnum):
    """Approval mode enum for enterprise execution safety."""

    AUTO = "AUTO"
    ASK = "ASK"
    READ_ONLY = "READ_ONLY"


class TaskStep(BaseModel):
    """Value object representing an atomic step in a plan."""

    model_config = ConfigDict(frozen=True)

    step_id: int = Field(..., description="Step sequence number")
    target_file: str = Field(..., description="Target file path")
    action_type: str = Field(..., description="Action type")
    description: str = Field(..., description="Step explanation")


class TaskPlan(BaseModel):
    """Aggregate plan representing multi-file task execution."""

    model_config = ConfigDict(frozen=True)

    plan_id: str = Field(..., description="Unique plan ID")
    goal: str = Field(..., description="User goal description")
    steps: list[TaskStep] = Field(default_factory=list)
    mode: ApprovalMode = Field(default=ApprovalMode.ASK)
    approved: bool = Field(default=False)
