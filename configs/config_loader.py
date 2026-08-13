from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field

"""Declarative Environment Configuration Loader Engine."""


class EnvironmentConfigDTO(BaseModel):
    """Value object representing an environment configuration snapshot."""

    model_config = ConfigDict(frozen=True)

    environment_name: str = Field(..., description="e.g. production, development")
    settings_data: dict[str, Any] = Field(default_factory=dict)
    policy_data: dict[str, Any] = Field(default_factory=dict)
    is_airgapped: bool = Field(default=False)


class ConfigurationLoaderEngine:
    """Engine loading declarative YAML configs for active environment."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path("D:/EAOS")).resolve()
        self.configs_dir = self.root / "configs"

    def load_environment_config(self, env_name: str = "production") -> EnvironmentConfigDTO:
        """Load YAML configuration for given environment."""
        env_dir = self.configs_dir / env_name
        settings_file = env_dir / "settings.yaml"

        settings_data: dict[str, Any] = {}
        if settings_file.exists():
            raw_text = settings_file.read_text(encoding="utf-8")
            settings_data = yaml.safe_load(raw_text) or {}

        policy_file = self.configs_dir / "governance_policy.yaml"
        policy_data: dict[str, Any] = {}
        if policy_file.exists():
            raw_pol = policy_file.read_text(encoding="utf-8")
            policy_data = yaml.safe_load(raw_pol) or {}

        return EnvironmentConfigDTO(
            environment_name=env_name,
            settings_data=settings_data,
            policy_data=policy_data,
            is_airgapped=env_name == "airgapped",
        )
