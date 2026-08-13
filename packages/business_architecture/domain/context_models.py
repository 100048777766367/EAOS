from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Context Engine Domain Models (Phase 1)."""


class SystemContextPayload(BaseModel):
    """Aggregate payload containing auto-injected context."""

    model_config = ConfigDict(frozen=True)

    constitution_text: str = Field(default="", description="Constitution v3.0 excerpt")
    adr_summaries: list[str] = Field(default_factory=list, description="ADR summaries")
    pyproject_specs: str = Field(default="", description="pyproject.toml excerpt")
    active_capability: str = Field(default="cap-control-room", description="Active capability")


class InjectedPromptContext(BaseModel):
    """Prompt decorated with full enterprise context."""

    model_config = ConfigDict(frozen=True)

    user_prompt: str
    context_payload: SystemContextPayload
    formatted_prompt: str
