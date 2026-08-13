from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

"""Dynamic Plugin Discovery and Management Engine."""


class ExtensionPluginDTO(BaseModel):
    """Value object representing a dynamic extension plugin."""

    model_config = ConfigDict(frozen=True)

    plugin_id: str = Field(..., description="Plugin canonical ID")
    title: str = Field(..., description="Plugin title")
    version: str = Field(default="1.0.0")
    author: str = Field(default="EAOS Ecosystem")
    is_enabled: bool = Field(default=True)


class DynamicPluginManager:
    """Manager discovering and hot-plugging extension plugins."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()
        self._plugins: dict[str, ExtensionPluginDTO] = {}
        self._register_default_plugins()

    def _register_default_plugins(self) -> None:
        p1 = ExtensionPluginDTO(
            plugin_id="plugin-devsecops-checker",
            title="DevSecOps Security Checker Plugin",
            version="1.0.0",
        )
        self._plugins[p1.plugin_id] = p1

    def register_plugin(self, plugin: ExtensionPluginDTO) -> None:
        """Register a new extension plugin."""
        self._plugins[plugin.plugin_id] = plugin

    def list_active_plugins(self) -> list[ExtensionPluginDTO]:
        """Return list of registered active plugins."""
        return list(self._plugins.values())
