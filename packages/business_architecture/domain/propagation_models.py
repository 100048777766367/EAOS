from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Change Propagation Domain Models (Phase 3)."""


class AffectedArtifact(BaseModel):
    """Value object representing an artifact affected by change."""

    model_config = ConfigDict(frozen=True)

    target_name: str = Field(..., description="Target ecosystem name")
    file_path: str = Field(..., description="File path affected")
    change_status: str = Field(..., description="MODIFIED, CREATED, DELETED")


class ImpactAnalysisMatrix(BaseModel):
    """Impact Matrix analyzing business change propagation."""

    model_config = ConfigDict(frozen=True)

    capability_id: str
    policy_id: str
    values_changed_count: int = Field(default=0)
    affected_artifacts: list[AffectedArtifact] = Field(default_factory=list)
    required_tests_count: int = Field(default=0)
