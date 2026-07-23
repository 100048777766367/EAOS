"""Data Transfer Objects for Policy Engine application layer."""

from typing import Any

from pydantic import BaseModel, Field

from packages.policy_engine.domain.models import Operator, PolicyEffect


class ConditionDTO(BaseModel):
    field_path: str
    operator: Operator
    expected_value: Any


class PolicyRuleDTO(BaseModel):
    rule_id: str
    name: str
    effect: PolicyEffect
    condition: ConditionDTO
    failure_message: str


class RegisterPolicyCommand(BaseModel):
    policy_id: str
    name: str
    description: str
    rules: list[PolicyRuleDTO] = Field(default_factory=list)


class EvaluatePolicyCommand(BaseModel):
    policy_id: str
    context_payload: dict[str, Any]


class PolicyEvaluationResultDTO(BaseModel):
    policy_id: str
    is_allowed: bool
    violations: list[dict[str, str]]
    evaluated_at: str
