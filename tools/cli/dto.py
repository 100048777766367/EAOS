from __future__ import annotations

from enum import IntEnum

from pydantic import BaseModel, ConfigDict, Field

"""Data Transfer Objects and Exit Codes for EAOS CLI."""


class CLIExitCode(IntEnum):
    """Standardized exit codes for EAOS CLI Commands."""

    HEALTHY = 0
    WARNING = 1
    FAILED = 2
    CRITICAL = 3
    CONFIG_ERROR = 4
    INTERNAL_ERROR = 5


class CLIContextDTO(BaseModel):
    """Context representation passed to CLI commands."""

    model_config = ConfigDict(frozen=True)

    workspace_root: str = Field(default="D:\\EAOS")
    verbose: bool = Field(default=False)
    output_format: str = Field(default="console")
    color_enabled: bool = Field(default=True)
