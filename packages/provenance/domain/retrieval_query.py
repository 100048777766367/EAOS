from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Domain Model for Structured Retrieval Queries."""


class RetrievalQuery(BaseModel):
    """Structured retrieval query DTO."""

    model_config = ConfigDict(frozen=True)

    user_id: str = Field(..., description="Enterprise semantic model field description")
    conversation_id: str | None = Field(default=None)
    session_id: str | None = Field(default=None)
    target_entities: list[str] = Field(default_factory=list)
    relation_types: list[str] = Field(default_factory=list)
    start_turn: int | None = Field(default=None)
    end_turn: int | None = Field(default=None)
    query_text: str = Field(default="")
