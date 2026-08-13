from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""Data Architecture Frameworks & Paradigms Domain Model."""


class DataFrameworkType(StrEnum):
    """Enumeration of 6 Data Architecture Frameworks & Paradigms."""

    DAMA_DMBOK = "DAMA_DMBOK"
    DCAM = "DCAM"
    EDM_CDMC = "EDM_CDMC"
    CMMI_DMM = "CMMI_DMM"
    DATA_MESH = "DATA_MESH"
    DATA_FABRIC = "DATA_FABRIC"


class DataGovernanceRule(BaseModel):
    """Value object representing an executable data governance policy."""

    model_config = ConfigDict(frozen=True)

    framework_type: DataFrameworkType
    rule_code: str
    domain_owner: str
    target_schema: str
    is_automated: bool = True


class DataFrameworkProfile(BaseModel):
    """Entity representing an ingested Data Architecture Profile."""

    model_config = ConfigDict(frozen=True)

    profile_id: str = Field(..., description="Unique Profile UUID")
    framework_type: DataFrameworkType
    name: str
    rules: tuple[DataGovernanceRule, ...] = ()
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
