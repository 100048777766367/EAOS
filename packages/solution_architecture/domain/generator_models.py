from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Code Generator Domain Models (Phase 3)."""


class GeneratedArtifact(BaseModel):
    """Value object representing a generated target artifact."""

    model_config = ConfigDict(frozen=True)

    target_name: str = Field(..., description="Target: python, rego, openapi, pytest")
    file_path: str = Field(..., description="Target output file path")
    content: str = Field(..., description="Generated code or spec content")


class MultiTargetCompilationResult(BaseModel):
    """Aggregate result of compiling IR to 4 targets."""

    model_config = ConfigDict(frozen=True)

    capability_id: str
    policy_id: str
    artifacts: list[GeneratedArtifact] = Field(default_factory=list)
