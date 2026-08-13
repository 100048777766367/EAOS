from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""Universal Enterprise Architecture Frameworks Domain Model.

Provides a Unifying Architecture Abstraction Layer supporting reference,
mapping, integration, and extension across 12 global EA categories.
"""


class FrameworkMetadataVO(BaseModel):
    """Value object representing an EA Framework's metadata."""

    model_config = ConfigDict(frozen=True)

    code: str
    name: str
    category: str
    description: str


class EAFrameworkType(StrEnum):
    """Enumeration of 16 supported Enterprise Architecture Frameworks."""

    TOGAF = "TOGAF"
    ZACHMAN = "ZACHMAN"
    FEAF = "FEAF"
    DODAF = "DODAF"
    MODAF = "MODAF"
    NAF = "NAF"
    UAF = "UAF"
    GARTNER = "GARTNER"
    PEAF = "PEAF"
    CAPSTERA = "CAPSTERA"
    DRAGON1 = "DRAGON1"
    E2AF = "E2AF"
    TRAK = "TRAK"
    SABSA = "SABSA"
    ARCHIMATE = "ARCHIMATE"
    RM_ODP = "RM_ODP"


class MetamodelMapping(BaseModel):
    """Value object mapping a framework metamodel element to EAOS."""

    model_config = ConfigDict(frozen=True)

    framework_type: EAFrameworkType
    element_name: str
    target_eaos_concept: str
    viewpoint_code: str


class FrameworkProfile(BaseModel):
    """Entity representing an ingested EA Framework Metamodel Profile."""

    model_config = ConfigDict(frozen=True)

    profile_id: str = Field(..., description="Unique Profile UUID")
    framework_type: EAFrameworkType
    name: str
    mappings: tuple[MetamodelMapping, ...] = ()
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
