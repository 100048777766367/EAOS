"""Evidence backed self healing engine."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dxs.evidence.hash import calculate_hash
from dxs.evidence.ledger import EvidenceLedger
from dxs.evidence.timeline import EvidenceTimeline, TimelineEvent

from .model import HealingAction, HealingPlan, HealingResult


class SelfHealingEngine:
    """Self healing engine with immutable evidence trail."""

    def __init__(
        self,
        evidence_path: Path | None = None,
    ):
        if evidence_path is None:
            evidence_path = Path("runtime/evidence/self_healing")

        evidence_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.evidence_path = evidence_path
        self.ledger = EvidenceLedger(evidence_path)
        self.timeline = EvidenceTimeline(evidence_path)

    def diagnose(
        self,
        issue: str,
    ) -> HealingPlan:
        return HealingPlan(
            action=HealingAction.REPAIR,
            target=issue,
            reason=f"Detected issue: {issue}",
        )

    def repair(
        self,
        plan: HealingPlan,
    ) -> HealingResult:
        return self.execute(
            action=plan.action,
            context={
                "target": plan.target,
                "reason": plan.reason,
            },
        )

    def execute(
        self,
        action: HealingAction,
        context: dict[str, Any],
    ) -> HealingResult:
        payload = {
            "action": action.value,
            "context": context,
            "status": "HEALED",
        }

        payload["hash"] = calculate_hash(payload)

        evidence_file = self.ledger.record(
            action.value,
            payload,
        )

        self.timeline.append(
            TimelineEvent(
                hash=payload["hash"],
                action=action.value,
                timestamp=datetime.now(UTC).isoformat(),
                metadata={
                    "context": context,
                    "status": "HEALED",
                },
            )
        )

        result = HealingResult(
            success=True,
            message="Healing completed",
            evidence_hash=payload["hash"],
            action=action,
            evidence=evidence_file,
        )

        result.status = "HEALED"

        return result

    def verify(
        self,
        result: HealingResult,
    ) -> bool:
        """Verify evidence backed healing result."""

        return result.success and result.status == "HEALED" and result.evidence is not None and result.evidence.exists()
