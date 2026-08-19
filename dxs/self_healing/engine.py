"""Domain execution semantics for DXS self healing."""

from __future__ import annotations

from pathlib import Path

from .model import HealingAction, HealingPlan, HealingResult, HealingStatus


class SelfHealingEngine:
    """Executes healing plans without owning application workflow gates."""

    def __init__(
        self,
        evidence_path: Path | None = None,
    ) -> None:
        self.evidence_path = evidence_path

    def diagnose(
        self,
        issue: str,
    ) -> HealingPlan:
        """Create a deterministic plan without mutating the target system."""

        return HealingPlan(
            action=HealingAction.REPAIR,
            target=issue,
            reason=f"Detected issue: {issue}",
            rollback_supported=False,
        )

    def repair(
        self,
        plan: HealingPlan,
    ) -> HealingResult:
        """Execute an already planned healing action."""

        return self.execute(
            action=plan.action,
            context={
                "target": plan.target,
                "reason": plan.reason,
            },
            rollback_supported=plan.rollback_supported,
        )

    def execute(
        self,
        action: HealingAction,
        context: dict[str, object],
        rollback_supported: bool = False,
    ) -> HealingResult:
        """Execute domain healing semantics without governance decisions."""

        if context.get("force_failure") is True:
            return HealingResult(
                success=False,
                message="Healing execution failed",
                action=action,
                status=HealingStatus.FAILED,
                rollback_supported=rollback_supported,
            )

        return HealingResult(
            success=True,
            message="Healing completed",
            action=action,
            status=HealingStatus.HEALED,
            rollback_supported=rollback_supported,
        )

    def verify(
        self,
        result: HealingResult,
    ) -> bool:
        """Verify successful domain execution semantics."""

        return result.success and result.status == HealingStatus.HEALED
