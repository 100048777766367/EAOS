from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

"""Domain Model for Temporal Hierarchy Tree."""


class TemporalHierarchy(BaseModel):
    """Temporal hierarchy node mapping Session -> Turn -> Evidence."""

    model_config = ConfigDict(frozen=True)

    user_id: str = Field(..., description="Enterprise semantic model field description")
    conversation_id: str = Field(..., description="Enterprise semantic model field description")
    session_id: str = Field(..., description="Enterprise semantic model field description")
    turn_id: int = Field(..., description="Enterprise semantic model field description")
    evidence_id: str = Field(..., description="Enterprise semantic model field description")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
