from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Domain Model for Evidence Source Tracking."""


class EvidenceSource(BaseModel):
    """Value object representing evidence origin source."""

    model_config = ConfigDict(frozen=True)

    source_name: str = Field(..., description="Enterprise semantic model field description")
    uri: str = Field(default="", description="Enterprise semantic model field description")
    actor: str = Field(default="OPERATOR", description="Enterprise semantic model field description")
