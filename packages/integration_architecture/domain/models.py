from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""Integration Architecture Frameworks & Patterns Domain Model."""


class IntegrationFrameworkType(StrEnum):
    """Enumeration of 6 Integration Architecture Patterns & Frameworks."""

    SOA_REF_ARCH = "SOA_REF_ARCH"
    EIP = "EIP"
    API_FIRST = "API_FIRST"
    EDA = "EDA"
    MICROSERVICES_REF_ARCH = "MICROSERVICES_REF_ARCH"
    SERVICE_MESH = "SERVICE_MESH"


class IntegrationContractPattern(BaseModel):
    """Value object representing an executable integration contract."""

    model_config = ConfigDict(frozen=True)

    framework_type: IntegrationFrameworkType
    pattern_code: str
    protocol: str
    endpoint_or_topic: str
    is_asynchronous: bool = False


class IntegrationFrameworkProfile(BaseModel):
    """Entity representing an ingested Integration Architecture Profile."""

    model_config = ConfigDict(frozen=True)

    profile_id: str = Field(..., description="Unique Profile UUID")
    framework_type: IntegrationFrameworkType
    name: str
    patterns: tuple[IntegrationContractPattern, ...] = ()
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
