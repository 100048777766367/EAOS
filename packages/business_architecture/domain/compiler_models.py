from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

"""Enterprise Model Compiler Domain Models (Phase 3)."""


class DecisionCondition(BaseModel):
    """Condition tuple for business decision rules."""

    model_config = ConfigDict(frozen=True)

    field: str = Field(..., description="Target field name e.g. customer_tier")
    operator: str = Field(..., description="Operator e.g. equals, >=")
    value: Any = Field(..., description="Comparison value e.g. GOLD")


class BusinessDecisionRule(BaseModel):
    """Decision rule in neutral specification."""

    model_config = ConfigDict(frozen=True)

    rule_id: str = Field(..., description="Unique rule ID")
    conditions: list[DecisionCondition] = Field(default_factory=list)
    discount_percentage: float = Field(default=0.0)
    maximum_discount: float = Field(default=0.0)
    currency: str = Field(default="VND")


class BusinessSpecificationIR(BaseModel):
    """Intermediate Representation (IR) for business specs."""

    model_config = ConfigDict(frozen=True)

    capability_id: str = Field(..., description="Business capability ID")
    policy_id: str = Field(..., description="Policy identifier")
    policy_name: str = Field(..., description="Canonical policy name")
    rules: list[BusinessDecisionRule] = Field(default_factory=list)
