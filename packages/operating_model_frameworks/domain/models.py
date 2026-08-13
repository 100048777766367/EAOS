from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""Capability & Operating Model Frameworks Domain Model for EAOS."""


class OperatingModelFrameworkType(StrEnum):
    """Enumeration of 7 Capability & Operating Model Frameworks."""

    CAPABILITY_MAP = "CAPABILITY_MAP"
    CMMI = "CMMI"
    OPERATING_MODEL_CANVAS = "OPERATING_MODEL_CANVAS"
    TEAM_TOPOLOGIES = "TEAM_TOPOLOGIES"
    VALUE_STREAM_MAPPING = "VALUE_STREAM_MAPPING"
    ORG_DESIGN = "ORG_DESIGN"
    ODI = "ODI"


class OperatingModelProfile(BaseModel):
    """Entity representing an ingested Operating Model Profile."""

    model_config = ConfigDict(frozen=True)

    profile_id: str = Field(..., description="Unique Profile ID")
    framework_type: OperatingModelFrameworkType
    name: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
