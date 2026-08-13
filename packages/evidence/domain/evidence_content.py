from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Domain Model for Raw Evidence Content Structure."""


class EvidenceContent(BaseModel):
    """Raw content structure with MIME type and size metadata."""

    model_config = ConfigDict(frozen=True)

    raw_content: str = Field(..., description="Enterprise semantic model field description")
    mime_type: str = Field(default="text/plain")
    encoding: str = Field(default="utf-8")
    size_bytes: int = Field(default=0)
