"""Engineering Intent Model converting raw user prompts into structured engineering goals."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class EngineeringIntentDTO:
    """Canonical representation of an engineering request intent."""

    intent_id: str
    raw_user_request: str
    interpreted_objective: str
    desired_outcome: str
    affected_subsystem: str
    success_criteria: list[str]
    non_goals: list[str]
    required_authority: str
    verification_requirements: list[str]
    confidence_score: float = 1.0
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class EngineeringIntentBuilder:
    """Parses user prompts and constructs unambiguous EngineeringIntentDTO."""

    @classmethod
    def build_intent(
        self,
        raw_request: str,
        target_subsystem: str = "general",
        required_authority: str = "L2",
    ) -> EngineeringIntentDTO:
        """Formulates structured engineering intent from raw user request."""
        import uuid

        intent_id = f"intent-{uuid.uuid4().hex[:8]}"

        # Infer objective
        clean_req = raw_request.strip()
        interpreted = f"Resolve engineering request: '{clean_req}'"

        # Success criteria
        success_criteria = [
            "Source code compiles clean",
            "Target subsystem tests pass",
            "Architecture invariants preserved",
            "Zero security boundary violations",
        ]

        # Non-goals (protect boundaries)
        non_goals = [
            "Do not modify ARCHITECTURE_CONSTITUTION.md or GOVERNANCE.md",
            "Do not alter public REST/WebSocket contracts unless authorized",
            "Do not execute mass ruff --fix rewrites",
        ]

        return EngineeringIntentDTO(
            intent_id=intent_id,
            raw_user_request=clean_req,
            interpreted_objective=interpreted,
            desired_outcome="System state restored to HEALTHY with verified evidence token",
            affected_subsystem=target_subsystem,
            success_criteria=success_criteria,
            non_goals=non_goals,
            required_authority=required_authority,
            verification_requirements=["unit_tests", "integration_tests", "clean_arch_check"],
        )
