from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""UI as a Capability & Meta-Layer Domain Models (ADR-UI-002)."""


class CommandPaletteAction(BaseModel):
    """Action executable via Command Palette (Ctrl+K / Ctrl+Shift+P)."""

    model_config = ConfigDict(frozen=True)

    action_id: str = Field(..., description="Action ID e.g. cmd-run-doctor")
    title: str = Field(..., description="Action title e.g. Run Doctor")
    category: str = Field(default="GOVERNANCE", description="Category")
    shortcut: str = Field(default="", description="Keyboard shortcut")


class PanelWidgetConfig(BaseModel):
    """Widget specification in Meta-Layer UI Model."""

    model_config = ConfigDict(frozen=True)

    widget_id: str
    widget_type: str = Field(..., description="CHAT, GRAPH, METRICS, DIFF")
    dock_position: str = Field(default="CENTER")
    visible: bool = Field(default=True)


class WorkspaceLayoutConfig(BaseModel):
    """Workspace Layout configuration for a specific Persona."""

    model_config = ConfigDict(frozen=True)

    workspace_id: str = Field(..., description="Workspace ID")
    persona_role: str = Field(default="architect")
    version: str = Field(default="1.0.0", description="Layout version")
    widgets: list[PanelWidgetConfig] = Field(default_factory=list)


class GlobalContextDTO(BaseModel):
    """Global Context always visible to AI and User."""

    model_config = ConfigDict(frozen=True)

    workspace_root: str = Field(default="D:\\EAOS")
    sprint: str = Field(default="Sprint 3.5")
    active_capability: str = Field(default="cap-control-room")
    current_adr: str = Field(default="ADR-UI-002")
    git_branch: str = Field(default="main")
    environment: str = Field(default="LOCAL_PROD")
