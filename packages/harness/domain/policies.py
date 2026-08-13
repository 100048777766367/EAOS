from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Domain Policy DTOs for Action Scope and Permissions."""


class ScopePolicyDTO(BaseModel):
    """Policy restricting filesystem and shell scope boundary."""

    model_config = ConfigDict(frozen=True)

    workspace_root: str = Field(..., description="Enterprise semantic model field description")
    allowed_file_extensions: list[str] = Field(
        default_factory=lambda: [
            ".py",
            ".md",
            ".json",
            ".yaml",
            ".yml",
            ".html",
            ".js",
        ]
    )
    allow_out_of_scope_read: bool = Field(default=False)
