from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

"""Decision Rules Evaluator Engine (DMN Pattern)."""


class RuleConditionDTO(BaseModel):
    """Condition tuple for decision rules."""

    model_config = ConfigDict(frozen=True)

    field: str = Field(..., description="Target field name e.g. amount")
    operator: str = Field(..., description="e.g. <, >=, equals")
    value: Any = Field(..., description="Value to compare")


class DecisionRuleDTO(BaseModel):
    """Value object representing a decision rule."""

    model_config = ConfigDict(frozen=True)

    rule_id: str = Field(..., description="Rule ID e.g. R01")
    name: str = Field(..., description="Rule name")
    conditions: list[RuleConditionDTO] = Field(default_factory=list)
    outcome: str = Field(..., description="Outcome or decision result")


class DecisionRuleEvaluator:
    """Evaluator executing deterministic decision rules."""

    def evaluate_rule(self, rule: DecisionRuleDTO, context: dict[str, Any]) -> bool:
        """Evaluate if context satisfies all rule conditions."""
        for cond in rule.conditions:
            ctx_val = context.get(cond.field)
            if ctx_val is None:
                return False
            if cond.operator == "<" and not (ctx_val < cond.value):
                return False
            if cond.operator == ">=" and not (ctx_val >= cond.value):
                return False
            if cond.operator == "equals" and ctx_val != cond.value:
                return False
        return True
