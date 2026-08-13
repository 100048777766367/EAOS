from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""EAOS Interaction Architecture Domain Contracts (ADR-UI-001)."""


class InteractionState(StrEnum):
    """Standardized interaction state machine enum."""

    UNKNOWN = "UNKNOWN"
    IDLE = "IDLE"
    DRAFT = "DRAFT"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    BLOCKED = "BLOCKED"
    PARTIALLY_COMPLETED = "PARTIALLY_COMPLETED"
    COMPLETED = "COMPLETED"
    WARNING = "WARNING"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"


class InteractionContextDTO(BaseModel):
    """Context representation for interaction execution."""

    model_config = ConfigDict(frozen=True)

    workspace: str = Field(default="D:\\EAOS")
    capability_id: str = Field(default="cap-control-room")
    domain: str = Field(default="interaction_architecture")
    environment: str = Field(default="LOCAL_PROD")
    user_role: str = Field(default="Chief Architect")
    approval_mode: str = Field(default="ASK")


class InteractionActionDTO(BaseModel):
    """Action specification in interaction contract."""

    model_config = ConfigDict(frozen=True)

    action_name: str = Field(..., description="Action name")
    risk_level: str = Field(default="LOW", description="Risk level")
    required_permission: str = Field(default="execute", description="Required permission")
    undoable: bool = Field(default=True, description="Can action be undone")


class InteractionEvidenceDTO(BaseModel):
    """Evidence model for auditing interaction execution."""

    model_config = ConfigDict(frozen=True)

    evidence_id: str = Field(..., description="Unique evidence ID")
    actor_id: str = Field(..., description="Actor or agent identifier")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    before_state_hash: str = Field(..., description="Hash before change")
    after_state_hash: str = Field(..., description="Hash after change")
    policy_applied: str = Field(..., description="Applied policy ID")
    approval_decision: str = Field(..., description="Decision record")


class InteractionContract(BaseModel):
    """Complete 6-part Interaction Contract specification."""

    model_config = ConfigDict(frozen=True)

    context: InteractionContextDTO
    state: InteractionState = Field(default=InteractionState.IDLE)
    action: InteractionActionDTO
    feedback_message: str = Field(default="Initialized")
    evidence: InteractionEvidenceDTO | None = None
    control_allowed: bool = Field(default=True)
