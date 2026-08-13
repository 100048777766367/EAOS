from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""Solution & Software Architecture Frameworks Domain Model."""


class SolutionPatternType(StrEnum):
    """Enumeration of 10 Solution & Software Architecture Standards."""

    DDD = "DDD"
    HEXAGONAL = "HEXAGONAL"
    CLEAN_ARCH = "CLEAN_ARCH"
    ONION_ARCH = "ONION_ARCH"
    PORTS_AND_ADAPTERS = "PORTS_AND_ADAPTERS"
    C4_MODEL = "C4_MODEL"
    ARC42 = "ARC42"
    ADR = "ADR"
    EVOLUTIONARY_ARCH = "EVOLUTIONARY_ARCH"
    TWELVE_FACTOR = "TWELVE_FACTOR"


class PatternComplianceRule(BaseModel):
    """Value object representing a software architecture pattern rule."""

    model_config = ConfigDict(frozen=True)

    pattern_type: SolutionPatternType
    rule_name: str
    target_layer: str
    is_enforced: bool = True


class SolutionArchitectureProfile(BaseModel):
    """Entity representing an ingested Solution Architecture Profile."""

    model_config = ConfigDict(frozen=True)

    profile_id: str = Field(..., description="Unique Profile UUID")
    pattern_type: SolutionPatternType
    name: str
    rules: tuple[PatternComplianceRule, ...] = ()
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
