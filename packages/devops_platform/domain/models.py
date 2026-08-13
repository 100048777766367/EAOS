from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""DevOps & Platform Engineering Frameworks Domain Model for EAOS."""


class DevOpsFrameworkType(StrEnum):
    """Enumeration of 7 DevOps & Platform Engineering Frameworks."""

    DEVOPS_HANDBOOK = "DEVOPS_HANDBOOK"
    GITOPS = "GITOPS"
    PLATFORM_ENGINEERING = "PLATFORM_ENGINEERING"
    IDP = "IDP"
    OPENGITOPS = "OPENGITOPS"
    OPENTELEMETRY = "OPENTELEMETRY"
    FINOPS = "FINOPS"


class DevOpsProfile(BaseModel):
    """Value object representing an ingested DevOps & Platform Profile."""

    model_config = ConfigDict(frozen=True)

    profile_id: str = Field(..., description="Unique Profile ID")
    framework_type: DevOpsFrameworkType
    name: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
