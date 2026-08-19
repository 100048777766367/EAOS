"""Application orchestration for DXS self healing."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

from dxs.evidence.hash import calculate_hash
from dxs.evidence.ledger import EvidenceLedger
from dxs.evidence.timeline import EvidenceTimeline, TimelineEvent
from dxs.governance.model import GovernanceDecision
from dxs.self_healing.engine import SelfHealingEngine
from dxs.self_healing.model import HealingAction, HealingResult, HealingStatus

ValidationCheck = Callable[[HealingResult], bool]


class SelfHealingOrchestrator:
    """Coordinates self-healing policy, governance, execution, and evidence."""

    def __init__(
        self,
        engine: SelfHealingEngine | None = None,
        evidence_path: Path | None = None,
        validation: ValidationCheck | None = None,
    ) -> None:
        if evidence_path is None:
            evidence_path = Path("runtime/evidence/self_healing")

        evidence_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.engine = engine or SelfHealingEngine()
        self.evidence_path = evidence_path
        self.ledger = EvidenceLedger(evidence_path)
        self.timeline = EvidenceTimeline(evidence_path)
        self.validation = validation

    def heal(
        self,
        issue: str,
        governance: GovernanceDecision | None = None,
        rollback_supported: bool = False,
        policy: str = "default_self_healing_policy",
        risk: str = "low",
    ) -> HealingResult:
        """Run detection, diagnosis, plan, execution, validation, evidence."""

        plan = self.engine.diagnose(issue)
        context = {
            "detection": issue,
            "diagnosis": plan.reason,
            "plan_target": plan.target,
            "policy": policy,
            "risk": risk,
        }

        return self.execute(
            action=plan.action,
            context=context,
            governance=governance,
            rollback_supported=rollback_supported or plan.rollback_supported,
        )

    def execute(
        self,
        action: HealingAction,
        context: dict[str, object],
        governance: GovernanceDecision | None = None,
        rollback_supported: bool = False,
        validation: ValidationCheck | None = None,
        policy: str = "default_self_healing_policy",
        risk: str = "low",
    ) -> HealingResult:
        """Execute the application self-healing lifecycle."""

        context = dict(context)
        context.setdefault("policy", policy)
        context.setdefault("risk", risk)
        decision = self._decision(governance)
        if not decision.allowed:
            return self._record_result(
                HealingResult(
                    success=False,
                    message=decision.reason,
                    action=action,
                    status=HealingStatus.BLOCKED,
                    rollback_supported=rollback_supported,
                ),
                context=context,
                governance=decision,
            )

        result = self.engine.execute(
            action=action,
            context=context,
            rollback_supported=rollback_supported,
        )
        check = validation or self.validation

        if result.success and check is not None and not check(result):
            result = HealingResult(
                success=False,
                message="Healing validation failed",
                action=action,
                status=HealingStatus.FAILED,
                rollback_supported=rollback_supported,
            )

        return self._record_result(
            result,
            context=context,
            governance=decision,
        )

    def _record_result(
        self,
        result: HealingResult,
        *,
        context: dict[str, object],
        governance: GovernanceDecision,
    ) -> HealingResult:
        payload = {
            "action": result.action.value if result.action else None,
            "context": context,
            "governance": {
                "allowed": governance.allowed,
                "reason": governance.reason,
                "rule": governance.rule,
            },
            "lineage": {
                "detected": context.get("detection"),
                "diagnosis": context.get("diagnosis"),
                "executed": result.status != HealingStatus.BLOCKED,
                "planned": result.action is not None,
                "policy": context.get("policy"),
                "risk": context.get("risk"),
                "validated": result.status == HealingStatus.HEALED,
            },
            "message": result.message,
            "rollback_supported": result.rollback_supported,
            "status": result.status.value,
        }
        payload["hash"] = calculate_hash(payload)
        evidence_file = self.ledger.record(result.status.value, payload)

        self.timeline.append(
            TimelineEvent(
                hash=str(payload["hash"]),
                action=result.status.value,
                timestamp=datetime.now(UTC).isoformat(),
                metadata=payload,
            )
        )

        result.evidence_hash = str(payload["hash"])
        result.evidence = evidence_file
        return result

    def _decision(
        self,
        governance: GovernanceDecision | None,
    ) -> GovernanceDecision:
        if governance is not None:
            return governance

        return GovernanceDecision(
            allowed=True,
            rule="default_allow_compatibility",
            reason="No explicit governance decision supplied.",
        )


__all__ = ["SelfHealingOrchestrator"]
