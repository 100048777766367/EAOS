from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""Audit Event DTO for Integrity Failure Tracking (Item 17 Fix)."""


def utc_now() -> datetime:
    """Returns current UTC time."""
    return datetime.now(UTC)


class IntegrityFailureAuditEventDTO(BaseModel):
    """Immutable audit event emitted when tamper or chain breach occurs."""

    model_config = ConfigDict(frozen=True)

    event_id: str = Field(..., description="Enterprise semantic model field description")
    evidence_id: str = Field(..., description="Enterprise semantic model field description")
    failure_type: str = Field(..., description="Enterprise semantic model field description")
    details: str = Field(..., description="Enterprise semantic model field description")
    timestamp: datetime = Field(default_factory=utc_now)
