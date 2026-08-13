from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

"""Domain models for Grounded Evidence & Temporal Identity (Rule R22)."""


class SourceType(StrEnum):
    """Supported evidence source types."""

    CODE_SYMBOL = "CODE_SYMBOL"
    GIT_COMMIT = "GIT_COMMIT"
    DOCUMENT = "DOCUMENT"
    RUNTIME_LOG = "RUNTIME_LOG"
    SESSION_EVENT = "SESSION_EVENT"


class EvidenceRef(BaseModel):
    """4-Tier Identity and Temporal Event Reference DTO."""

    model_config = ConfigDict(frozen=True)

    user_id: str = Field(..., description="Enterprise semantic model field description")
    session_id: str = Field(..., description="Enterprise semantic model field description")
    conversation_id: str = Field(default="conv-default")
    message_id: str = Field(default="msg-000")
    task_id: str = Field(default="task-default")
    sequence: int = Field(default=1)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Evidence(BaseModel):
    """Verified Grounded Evidence Object DTO."""

    model_config = ConfigDict(frozen=True)

    evidence_id: str = Field(..., description="Enterprise semantic model field description")
    source_type: SourceType = Field(default=SourceType.CODE_SYMBOL)
    source_uri: str = Field(..., description="Enterprise semantic model field description")
    file_path: str | None = Field(default=None)
    line_start: int | None = Field(default=None)
    line_end: int | None = Field(default=None)
    content_hash: str = Field(default="hash-v1")
    repository_commit: str | None = Field(default=None)
    ref_identity: EvidenceRef | None = Field(default=None)
    content: str = Field(..., description="Enterprise semantic model field description")
    relevance_score: float = Field(default=0.95)
    authority_score: float = Field(default=1.0)
    freshness_score: float = Field(default=1.0)
    is_verified: bool = Field(default=True)
    metadata: dict[str, Any] = Field(default_factory=dict)


class EvidenceBundleDTO(BaseModel):
    """Grounded Evidence Bundle passed to LLM Prompt Context."""

    model_config = ConfigDict(frozen=True)

    bundle_id: str = Field(..., description="Enterprise semantic model field description")
    query_text: str = Field(..., description="Enterprise semantic model field description")
    user_identity: str = Field(..., description="Enterprise semantic model field description")
    session_identity: str = Field(..., description="Enterprise semantic model field description")
    trusted_evidences: list[Evidence] = Field(default_factory=list)
    total_evidences_verified: int = Field(default=0)
    confidence_score: float = Field(default=1.0)
