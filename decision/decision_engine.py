"""Decision intelligence engine evaluating rules and optimization models."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class DecisionOutcomeDTO(BaseModel):
    """Value object representing a decision engine evaluation outcome."""

    model_config = ConfigDict(frozen=True)

    decision_id: str
    rule_name: str
    passed: bool
    action: str


class DecisionIntelligenceEngine:
    """Engine executing rule evaluation, planning, and simulation."""

    def evaluate_decision(
        self,
        context: dict[str, Any],
    ) -> DecisionOutcomeDTO:
        """Evaluates decision rules against provided execution context."""
        env = str(context.get("env", "production"))
        passed = env == "production"

        return DecisionOutcomeDTO(
            decision_id="DEC-001",
            rule_name="Production Environment Gate",
            passed=passed,
            action="ALLOW" if passed else "BLOCK",
        )
