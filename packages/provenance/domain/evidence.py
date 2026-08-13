from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

"""Domain Model for Grounded Evidence without AI Summaries (Rule R42)."""


class SourceType(StrEnum):
    """Enumeration of valid evidence source types."""

    CONVERSATION = "CONVERSATION"
    CODE_SYMBOL = "CODE_SYMBOL"
    GIT_COMMIT = "GIT_COMMIT"
    DOCUMENT = "DOCUMENT"
    RUNTIME_LOG = "RUNTIME_LOG"
    TEST_RESULT = "TEST_RESULT"


class Evidence(BaseModel):
    """Core Grounded Evidence Entity DTO - Single Source of Truth."""

    model_config = ConfigDict(frozen=True)

    evidence_id: str = Field(..., description="Enterprise semantic model field description")
    user_id: str = Field(..., description="Enterprise semantic model field description")
    session_id: str = Field(..., description="Enterprise semantic model field description")
    conversation_id: str = Field(default="conv-001")
    turn_id: int = Field(..., description="Enterprise semantic model field description")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_type: SourceType = Field(default=SourceType.CONVERSATION)
    source_uri: str = Field(default="", description="Enterprise semantic model field description")
    content: str = Field(..., description="Enterprise semantic model field description")
    content_hash: str = Field(..., description="Enterprise semantic model field description")
    metadata: dict[str, Any] = Field(default_factory=dict)
