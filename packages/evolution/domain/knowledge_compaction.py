from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""Knowledge Compaction and Eviction Domain Models (100-Year Anti-Bloat)."""


class RawObservation(BaseModel):
    """Short-term raw observation event."""

    model_config = ConfigDict(frozen=True)

    obs_id: str = Field(..., description="Unique observation ID")
    event_type: str = Field(..., description="FAILED_PATCH, NO_CHANGE")
    raw_payload: str = Field(..., description="Raw log or patch text")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class CompactionSummary(BaseModel):
    """Distilled knowledge extracted from raw observations."""

    model_config = ConfigDict(frozen=True)

    capability_id: str
    total_raw_purged: int = Field(default=0)
    negative_lessons_extracted: list[str] = Field(default_factory=list)
    distilled_pattern: str = Field(default="")
    retained_size_bytes: int = Field(default=0)
