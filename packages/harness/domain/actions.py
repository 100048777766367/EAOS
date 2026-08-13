from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

"""Domain DTOs for Actions and Intent Compilation (Rule R35)."""


class SemanticActionType(StrEnum):
    """Semantic classifications for agent intents."""

    FS_READ = "FS_READ"
    FS_WRITE = "FS_WRITE"
    FS_DELETE = "FS_DELETE"
    SHELL_READ = "SHELL_READ"
    SHELL_DESTRUCTIVE = "SHELL_DESTRUCTIVE"
    GIT_MUTATE = "GIT_MUTATE"
    DB_MUTATE = "DB_MUTATE"
    SECRET_ACCESS = "SECRET_ACCESS"


class ActionIntentDTO(BaseModel):
    """Raw action intent submitted by Model."""

    model_config = ConfigDict(frozen=True)

    action_name: str = Field(..., description="Enterprise semantic model field description")
    target_uri: str = Field(..., description="Enterprise semantic model field description")
    payload: dict[str, Any] = Field(default_factory=dict)


class ValidatedActionDTO(BaseModel):
    """Compiled and scope-checked action ready for execution."""

    model_config = ConfigDict(frozen=True)

    action_id: str = Field(..., description="Enterprise semantic model field description")
    semantic_type: SemanticActionType = Field(default=SemanticActionType.FS_READ)
    target_uri: str = Field(..., description="Enterprise semantic model field description")
    payload: dict[str, Any] = Field(default_factory=dict)
    is_destructive: bool = Field(default=False)
    requires_checkpoint: bool = Field(default=True)
