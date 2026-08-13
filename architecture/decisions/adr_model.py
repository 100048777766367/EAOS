from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""Architecture Decision Records (ADR) Domain Models."""


class ADRStatus(StrEnum):
    """ADR Lifecycle Status Enum."""

    PROPOSED = "PROPOSED"
    RATIFIED = "RATIFIED"
    DEPRECATED = "DEPRECATED"
    SUPERSEDED = "SUPERSEDED"
    REJECTED = "REJECTED"


class ADRRecord(BaseModel):
    """Value object representing an Architecture Decision Record."""

    model_config = ConfigDict(frozen=True)

    adr_id: str = Field(..., description="Unique ADR ID e.g. ADR-UI-001")
    title: str = Field(..., description="ADR Title")
    status: ADRStatus = Field(default=ADRStatus.PROPOSED)
    author: str = Field(default="Architecture Review Board")
    context: str = Field(default="", description="Business context")
    decision: str = Field(default="", description="Architectural decision")
    consequences: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
