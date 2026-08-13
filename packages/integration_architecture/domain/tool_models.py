from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

"""Native Tool Calling Domain Models (Phase 1)."""


class ToolExecutionRequest(BaseModel):
    """Tool execution input payload."""

    model_config = ConfigDict(frozen=True)

    tool_name: str = Field(..., description="Tool canonical identifier")
    arguments: dict[str, Any] = Field(default_factory=dict, description="Execution arguments")


class ToolExecutionResult(BaseModel):
    """Tool execution output response."""

    model_config = ConfigDict(frozen=True)

    success: bool = Field(..., description="Execution status")
    tool_name: str = Field(..., description="Target tool name")
    output: str = Field(default="", description="Captured stdout/stderr")
    error: str | None = Field(default=None, description="Error detail")
