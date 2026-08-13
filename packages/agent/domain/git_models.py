from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Git Agent Domain Models (Phase 4 / Level 10)."""


class GitOperationResult(BaseModel):
    """Result of Git operation (branch, commit, push, PR)."""

    model_config = ConfigDict(frozen=True)

    success: bool = Field(..., description="Operation status")
    branch_name: str = Field(default="", description="Git branch")
    commit_hash: str = Field(default="", description="Commit SHA")
    commit_message: str = Field(default="", description="Commit message")
    pr_url: str = Field(default="", description="Pull Request URL")
    error: str | None = Field(default=None, description="Error detail")
