from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""Patch Engine Domain Models (Phase 1)."""


class BackupRecord(BaseModel):
    """Value object representing a file backup entry."""

    model_config = ConfigDict(frozen=True)

    original_path: str = Field(..., description="Original file path")
    backup_path: str = Field(..., description="Backup file path")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class PatchResult(BaseModel):
    """Result object of a unified patch operation."""

    model_config = ConfigDict(frozen=True)

    success: bool = Field(..., description="Success flag")
    target_file: str = Field(..., description="Target file path")
    diff_summary: str = Field(default="", description="Unified diff")
    backup: BackupRecord | None = Field(default=None, description="Backup record")
    error_message: str | None = Field(default=None, description="Error detail")
