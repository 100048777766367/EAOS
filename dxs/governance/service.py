from __future__ import annotations

from dxs.governance.model import GovernanceDecision


class GovernanceService:
    """Evaluates repository actions against governance rules."""

    def evaluate(
        self,
        *,
        rule: str,
        allowed: bool,
        reason: str,
    ) -> GovernanceDecision:
        return GovernanceDecision(
            allowed=allowed,
            rule=rule,
            reason=reason,
        )


__all__ = ["GovernanceService"]
