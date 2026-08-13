from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""Domain States for EAOS Harness."""


class TurnState(StrEnum):
    CREATED = "CREATED"
    RESTORED = "RESTORED"
    CONTEXT_READY = "CONTEXT_READY"
    DECIDING = "DECIDING"
    PROPOSED = "PROPOSED"
    VALIDATING = "VALIDATING"
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"
    EXECUTING = "EXECUTING"
    OBSERVING = "OBSERVING"
    VERIFYING = "VERIFYING"
    RECOVERING = "RECOVERING"
    ROLLED_BACK = "ROLLED_BACK"
    COMMITTED = "COMMITTED"


class ActionState(StrEnum):
    """Action state machine."""

    PROPOSED = "PROPOSED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class VerificationState(StrEnum):
    """Verification state machine."""

    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"


class RecoveryState(StrEnum):
    """Recovery state machine."""

    NONE = "NONE"
    TRIGGERED = "TRIGGERED"
    RESOLVED = "RESOLVED"


class ActionGateDecision(BaseModel):
    """Decision DTO emitted by Action Gate."""

    model_config = ConfigDict(frozen=True)
    approved: bool = Field(..., description="Enterprise semantic model field description")
    reason: str = Field(default="", description="Enterprise semantic model field description")
