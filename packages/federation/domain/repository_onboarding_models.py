from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""External Repository Onboarding Domain Models."""


class StackType(StrEnum):
    """Auto-detected technology stack for external repositories."""

    PYTHON = "PYTHON"
    NODEJS = "NODEJS"
    DOCKER = "DOCKER"
    UNKNOWN = "UNKNOWN"


class ExternalRepositoryDTO(BaseModel):
    """Value object representing an onboarded external repository."""

    model_config = ConfigDict(frozen=True)

    repo_name: str = Field(..., description="Repo canonical name e.g. strix")
    repo_url: str = Field(..., description="Git URL or GitHub slug")
    stack_type: StackType = Field(default=StackType.PYTHON)
    installed_path: str = Field(..., description="Local installation path")
    is_active: bool = Field(default=True)
    installed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class OnboardingReportDTO(BaseModel):
    """Report returned after onboarding an external repository."""

    model_config = ConfigDict(frozen=True)

    success: bool = Field(default=True)
    repo_name: str
    stack_type: StackType
    capability_id: str
    installation_log: str
