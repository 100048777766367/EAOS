from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""IT Management & Governance Frameworks Domain Model for EAOS."""


class ITGovernanceFrameworkType(StrEnum):
    """Enumeration of 6 IT Management and Governance Frameworks."""

    ITIL = "ITIL"
    COBIT = "COBIT"
    ISO_38500 = "ISO_38500"
    MOF = "MOF"
    VERISM = "VERISM"
    FITSM = "FITSM"


class ITControlObjective(BaseModel):
    """Value object representing an IT control or service management rule."""

    model_config = ConfigDict(frozen=True)

    framework_type: ITGovernanceFrameworkType
    control_code: str
    title: str
    target_service: str
    enforced: bool = True


class ITGovernanceProfile(BaseModel):
    """Entity representing an ingested IT Management Profile."""

    model_config = ConfigDict(frozen=True)

    profile_id: str = Field(..., description="Unique Profile UUID")
    framework_type: ITGovernanceFrameworkType
    name: str
    controls: tuple[ITControlObjective, ...] = ()
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
