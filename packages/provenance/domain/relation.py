from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Domain Model for Directed Relationship Edges."""


class Relation(BaseModel):
    """Directed relationship edge connecting entities to evidence."""

    model_config = ConfigDict(frozen=True)

    relation_id: str = Field(..., description="Enterprise semantic model field description")
    source_entity_id: str = Field(..., description="Enterprise semantic model field description")
    relation_type: str = Field(..., description="Enterprise semantic model field description")
    target_entity_id: str = Field(..., description="Enterprise semantic model field description")
    evidence_id: str = Field(..., description="Enterprise semantic model field description")
    turn_id: int = Field(..., description="Enterprise semantic model field description")
