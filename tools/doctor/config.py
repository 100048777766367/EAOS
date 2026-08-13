from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field

"""Declarative Configuration for Enterprise Doctor."""


class CategoryWeightConfig(BaseModel):
    """Configuration weights for diagnostic categories."""

    model_config = ConfigDict(frozen=True)

    runtime: float = Field(default=0.20)
    architecture: float = Field(default=0.30)
    infrastructure: float = Field(default=0.25)
    governance: float = Field(default=0.15)
    filesystem: float = Field(default=0.10)


class DoctorConfig(BaseModel):
    """Root configuration model for Doctor Engine."""

    model_config = ConfigDict(frozen=True)

    weights: CategoryWeightConfig = Field(default_factory=CategoryWeightConfig)
    disabled_checkers: list[str] = Field(default_factory=list)

    @classmethod
    def load_from_file(cls, config_path: Path) -> DoctorConfig:
        """Load doctor configuration from YAML file."""
        if not config_path.exists():
            return cls()
        try:
            data: dict[str, Any] = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
            return cls.model_validate(data)
        except Exception:
            return cls()
