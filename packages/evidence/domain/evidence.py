"""Domain Model for Grounded Evidence Entity v2 (Item 10 Timezone Fix)."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

from packages.evidence.domain.evidence_content import EvidenceContent
from packages.evidence.domain.evidence_id import EvidenceId
from packages.evidence.domain.evidence_integrity import (
    EvidenceIntegrityDTO,
)
from packages.evidence.domain.evidence_metadata import EvidenceMetadata
from packages.evidence.domain.evidence_source import EvidenceSource
from packages.evidence.domain.evidence_type import EvidenceType


def current_utc_time() -> datetime:
    """Returns timezone-aware current UTC datetime."""
    return datetime.now(UTC)


class Evidence(BaseModel):
    """Core Grounded Evidence Entity DTO - Zero AI Summaries & Timezone Aware."""

    model_config = ConfigDict(frozen=True)

    evidence_id: EvidenceId = Field(..., description="Enterprise semantic model field description")
    evidence_type: EvidenceType = Field(default=EvidenceType.CONVERSATION_TURN)
    user_id: str = Field(..., description="Enterprise semantic model field description")
    session_id: str = Field(..., description="Enterprise semantic model field description")
    turn_id: int = Field(..., description="Enterprise semantic model field description")
    source: EvidenceSource = Field(..., description="Enterprise semantic model field description")
    content: EvidenceContent = Field(..., description="Enterprise semantic model field description")
    metadata: EvidenceMetadata = Field(..., description="Enterprise semantic model field description")
    integrity: EvidenceIntegrityDTO = Field(..., description="Enterprise semantic model field description")
    captured_at: datetime = Field(default_factory=current_utc_time)
