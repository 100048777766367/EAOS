"""Enterprise Governance Domain Model for EAOS Constitution."""

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ArchitecturalMaturityLevel(StrEnum):
    """Five levels of Enterprise Architectural Maturity."""

    LEVEL_1_STATIC = "STATIC"
    LEVEL_2_EXECUTABLE = "EXECUTABLE"
    LEVEL_3_OBSERVABLE = "OBSERVABLE"
    LEVEL_4_ADAPTIVE = "ADAPTIVE"
    LEVEL_5_EVOLUTIONARY = "EVOLUTIONARY"


class ConstitutionalRule(BaseModel):
    """Value object representing an invariant architecture rule."""

    model_config = ConfigDict(frozen=True)

    rule_id: str = Field(..., description="Unique rule code, e.g. R01")
    title: str = Field(..., description="Rule title")
    statement: str = Field(..., description="Formal rule statement")
    enforced: bool = Field(default=True)


class ConstitutionAmendment(BaseModel):
    """Entity representing a proposed amendment to constitution."""

    model_config = ConfigDict(frozen=True)

    amendment_id: str
    target_rule: str
    proposed_text: str
    reasoning: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
