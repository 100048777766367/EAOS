from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Design Tokens Domain Models (ADR-UI-001)."""


class SemanticColorTokens(BaseModel):
    """Semantic color tokens mapping meaning rather than concrete hex."""

    model_config = ConfigDict(frozen=True)

    status_success: str = Field(default="emerald-400")
    status_warning: str = Field(default="amber-400")
    status_critical: str = Field(default="rose-400")
    action_primary: str = Field(default="emerald-600")
    surface_default: str = Field(default="slate-950")
    surface_panel: str = Field(default="slate-900")
    text_muted: str = Field(default="slate-400")
    border_focus: str = Field(default="emerald-500")


class DesignTokenRegistry(BaseModel):
    """Design Token Registry aggregate."""

    model_config = ConfigDict(frozen=True)

    version: str = Field(default="1.0.0")
    colors: SemanticColorTokens = Field(default_factory=SemanticColorTokens)
