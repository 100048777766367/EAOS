from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""Architecture Modeling Standards Domain Model for EAOS."""


class ModelingStandardType(StrEnum):
    """Enumeration of 9 Architecture Modeling Standards."""

    ARCHIMATE = "ARCHIMATE"
    UML = "UML"
    SYSML = "SYSML"
    BPMN = "BPMN"
    DMN = "DMN"
    CMMN = "CMMN"
    ERD = "ERD"
    IDEF0 = "IDEF0"
    IDEF1X = "IDEF1X"


class ModelingStandardProfile(BaseModel):
    """Entity representing an ingested Architecture Modeling Standard."""

    model_config = ConfigDict(frozen=True)

    profile_id: str = Field(..., description="Unique Profile ID")
    standard_type: ModelingStandardType
    name: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
