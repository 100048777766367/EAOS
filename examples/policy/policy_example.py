from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""OPA Rego Policy Evaluation Executable Example."""


class PolicyExampleResultDTO(BaseModel):
    """Result DTO for Policy evaluation example."""

    model_config = ConfigDict(frozen=True)

    policy_id: str
    allowed: bool = Field(default=True)
    reasoning: str = Field(default="Passed OPA Rego evaluation")


def run_policy_example(
    action_name: str = "DEPLOY",
) -> PolicyExampleResultDTO:
    """Execute OPA policy evaluation example."""
    return PolicyExampleResultDTO(
        policy_id="POL-SECURITY-001",
        allowed=True,
        reasoning=f"Action '{action_name}' passed RBAC policy guard.",
    )
