from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

"""Domain Model for Relation View Entities."""


class Entity(BaseModel):
    """Entity node for deterministic relationship graph."""

    model_config = ConfigDict(frozen=True)

    entity_id: str = Field(..., description="Enterprise semantic model field description")
    canonical_name: str = Field(..., description="Enterprise semantic model field description")
    entity_type: str = Field(default="CONCEPT")
    first_seen: datetime = Field(default_factory=datetime.utcnow)
    last_seen: datetime = Field(default_factory=datetime.utcnow)
