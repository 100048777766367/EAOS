from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""Architectural Lineage and Provenance Tracking Engine."""


class LineageRecordDTO(BaseModel):
    """Value object representing an architectural lineage record."""

    model_config = ConfigDict(frozen=True)

    record_id: str = Field(..., description="Unique record ID")
    entity_name: str = Field(..., description="Entity e.g. Rule R01")
    version: str = Field(default="1.0.0")
    parent_version: str | None = Field(default=None)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ArchitecturalLineageTracker:
    """Tracker logging architectural evolution lineage over 100 years."""

    def record_lineage(
        self,
        entity_name: str,
        version: str,
        parent_version: str | None = None,
    ) -> LineageRecordDTO:
        """Record lineage entry for an architectural element."""
        return LineageRecordDTO(
            record_id=f"lin-{entity_name.lower().replace(' ', '-')}",
            entity_name=entity_name,
            version=version,
            parent_version=parent_version,
        )
