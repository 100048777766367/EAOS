from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""Security Architecture Frameworks & Standards Domain Model."""


class SecurityFrameworkType(StrEnum):
    """Enumeration of 7 Security Architecture Frameworks & Standards."""

    SABSA = "SABSA"
    NIST_CSF = "NIST_CSF"
    NIST_RMF = "NIST_RMF"
    ISO_27001 = "ISO_27001"
    ISO_27002 = "ISO_27002"
    ZERO_TRUST_NIST800_207 = "ZERO_TRUST_NIST800_207"
    CIS_CONTROLS = "CIS_CONTROLS"


class SecurityControlPolicy(BaseModel):
    """Value object representing an executable security control rule."""

    model_config = ConfigDict(frozen=True)

    framework_type: SecurityFrameworkType
    control_id: str
    title: str
    rego_policy_path: str
    is_automated: bool = True


class SecurityFrameworkProfile(BaseModel):
    """Entity representing an ingested Security Architecture Profile."""

    model_config = ConfigDict(frozen=True)

    profile_id: str = Field(..., description="Unique Profile UUID")
    framework_type: SecurityFrameworkType
    name: str
    controls: tuple[SecurityControlPolicy, ...] = ()
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
