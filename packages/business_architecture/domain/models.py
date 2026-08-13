from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""Business Architecture Frameworks & Metamodels for EAOS."""


class BusinessFrameworkType(StrEnum):
    """Enumeration of 10 Business Architecture Frameworks."""

    BIZBOK = "BIZBOK"
    APQC_PCF = "APQC_PCF"
    VRM = "VRM"
    BMM = "BMM"
    CBP = "CBP"
    VALUE_STREAM = "VALUE_STREAM"
    OPERATING_MODEL_CANVAS = "OPERATING_MODEL_CANVAS"
    BUSINESS_MODEL_CANVAS = "BUSINESS_MODEL_CANVAS"
    LEAN_CANVAS = "LEAN_CANVAS"
    WARDLEY_MAPPING = "WARDLEY_MAPPING"


class BusinessElementMapping(BaseModel):
    """Value object mapping a business framework element to EAOS."""

    model_config = ConfigDict(frozen=True)

    framework_type: BusinessFrameworkType
    element_name: str
    target_eaos_concept: str


class BusinessFrameworkProfile(BaseModel):
    """Entity representing an ingested Business Architecture Model."""

    model_config = ConfigDict(frozen=True)

    profile_id: str = Field(..., description="Unique Profile UUID")
    framework_type: BusinessFrameworkType
    name: str
    mappings: tuple[BusinessElementMapping, ...] = ()
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
