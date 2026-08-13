from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

"""Domain Model for Audit Provenance Record Traceability."""


class ProvenanceRecord(BaseModel):
    """Audit record tracing evidence to its origin event chain."""

    model_config = ConfigDict(frozen=True)

    evidence_id: str = Field(..., description="Enterprise semantic model field description")
    parent_evidence_id: str | None = Field(default=None)
    actor: str = Field(..., description="Enterprise semantic model field description")
    operation: str = Field(..., description="Enterprise semantic model field description")
    tool_name: str | None = Field(default=None)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    content_hash: str = Field(..., description="Enterprise semantic model field description")
