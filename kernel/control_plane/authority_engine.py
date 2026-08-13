"""EAOS Bounded Autonomy Authority Engine."""

from __future__ import annotations

from enum import IntEnum

from pydantic import BaseModel


class AuthorityLevel(IntEnum):
    """The 8 Levels of Bounded Autonomy in EAOS."""

    L0_OBSERVE = 0
    L1_DIAGNOSE = 1
    L2_PATCH = 2
    L3_REFACTOR = 3
    L4_REWRITE_IMPLEMENTATION = 4
    L5_RECOVER_REPOSITORY = 5
    L6_ARCHITECTURE_CHANGE = 6
    L7_GOVERNANCE_CHANGE = 7


class AuthorityCheckResult(BaseModel):
    """Result of an authority evaluation."""

    authorized: bool
    requested_level: AuthorityLevel
    allowed_max_level: AuthorityLevel
    requires_human_approval: bool
    requires_adr_proposal: bool
    reason: str


class AuthorityEngine:
    """Authority Engine enforcing Bounded Autonomy (L0 - L7)."""

    # Maximum autonomous authority level granted to AI without human intervention
    MAX_AUTONOMOUS_LEVEL: AuthorityLevel = AuthorityLevel.L5_RECOVER_REPOSITORY

    def __init__(self, max_autonomous_level: AuthorityLevel = MAX_AUTONOMOUS_LEVEL) -> None:
        self.max_autonomous_level = max_autonomous_level

    def evaluate_authority(self, requested_level: AuthorityLevel) -> AuthorityCheckResult:
        """Evaluate whether a requested action level is authorized for autonomous execution."""
        if requested_level <= self.max_autonomous_level:
            reason = (
                f"Requested level '{requested_level.name}' is within "
                f"autonomous authority bound (<= {self.max_autonomous_level.name})."
            )
            return AuthorityCheckResult(
                authorized=True,
                requested_level=requested_level,
                allowed_max_level=self.max_autonomous_level,
                requires_human_approval=False,
                requires_adr_proposal=False,
                reason=reason,
            )

        requires_adr = requested_level == AuthorityLevel.L6_ARCHITECTURE_CHANGE
        adr_msg = "An ADR proposal is required." if requires_adr else "Human authority required."
        reason = (
            f"Requested level '{requested_level.name}' exceeds maximum "
            f"autonomous authority bound ({self.max_autonomous_level.name}). {adr_msg}"
        )
        return AuthorityCheckResult(
            authorized=False,
            requested_level=requested_level,
            allowed_max_level=self.max_autonomous_level,
            requires_human_approval=True,
            requires_adr_proposal=requires_adr,
            reason=reason,
        )
