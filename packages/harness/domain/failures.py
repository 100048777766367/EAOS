from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""Domain DTOs for Failure Classification and Recovery (Rule R36)."""


class FailureCategory(StrEnum):
    """Classifications for execution and verification failures."""

    NONE = "NONE"
    TRANSIENT = "TRANSIENT"
    TOOL_FAILURE = "TOOL_FAILURE"
    WRONG_ASSUMPTION = "WRONG_ASSUMPTION"
    TEST_FAILURE = "TEST_FAILURE"
    POLICY_VIOLATION = "POLICY_VIOLATION"
    INVARIANT_BREACH = "INVARIANT_BREACH"


class FailureReportDTO(BaseModel):
    """Detailed failure classification report."""

    model_config = ConfigDict(frozen=True)

    category: FailureCategory = Field(default=FailureCategory.NONE)
    description: str = Field(..., description="Enterprise semantic model field description")
    requires_rollback: bool = Field(default=False)
    failed_invariants: list[str] = Field(default_factory=list)

    @property
    def is_success(self) -> bool:
        return False
