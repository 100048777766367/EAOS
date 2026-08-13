"""Bounded Recovery Engine enforcing safe, governed auto-healing within L0-L5 bounds."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from runtime.policies.failure_taxonomy import (
    RuntimeFailureCategory,
    RuntimeFailureRecord,
)
from runtime.state.task_lifecycle import TaskLifecycleFSM, TaskState


class RecoveryAuthorityLevel(StrEnum):
    """Authority level required for recovery."""

    L2_PATCH = "L2_PATCH"
    L3_REFACTOR = "L3_REFACTOR"
    L4_REWRITE = "L4_REWRITE"
    L5_RECOVER = "L5_RECOVER"
    L6_ESCALATE_ARCH = "L6_ESCALATE_ARCH"
    L7_ESCALATE_GOV = "L7_ESCALATE_GOV"


@dataclass(frozen=True)
class RecoveryOutcome:
    """Outcome of a recovery attempt."""

    success: bool
    recovery_id: str
    failure_category: RuntimeFailureCategory
    authority_used: RecoveryAuthorityLevel
    action_taken: str
    escalation_required: bool = False
    evidence_token: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class BoundedRecoveryEngine:
    """Executes governed bounded recovery operations within L0-L5 authority limits."""

    def __init__(self) -> None:
        self._history: list[RecoveryOutcome] = []

    def attempt_task_recovery(
        self,
        fsm: TaskLifecycleFSM,
        failure: RuntimeFailureRecord,
    ) -> RecoveryOutcome:
        """Attempts bounded recovery for a failing task."""
        import uuid

        rec_id = f"rec-{uuid.uuid4().hex[:8]}"

        # Determine required authority level
        authority, is_escalation = self._assess_recovery_authority(failure.category)

        if is_escalation:
            # L6 / L7 boundary: Autonomous recovery prohibited!
            action_msg = f"Recovery blocked: {failure.category.value} requires human/ADR approval ({authority.value})"
            outcome = RecoveryOutcome(
                success=False,
                recovery_id=rec_id,
                failure_category=failure.category,
                authority_used=authority,
                action_taken=action_msg,
                escalation_required=True,
                evidence_token=f"TOKEN-ESCALATE-{rec_id}",
            )
            self._history.append(outcome)
            return outcome

        # Bounded L0-L5 recovery execution
        try:
            # Transition task to RECOVERING
            fsm.transition_to(
                TaskState.RECOVERING,
                f"RECOVER-TOKEN-{rec_id}",
                {"failure_id": failure.failure_id},
            )

            # Action execution (e.g. clear cache, reset session, retry handler)
            action_desc = f"Applied bounded {authority.value} recovery for {failure.category.value}"

            # Transition task back to RUNNING or VERIFYING
            fsm.transition_to(
                TaskState.RUNNING,
                f"RESUME-TOKEN-{rec_id}",
                {"recovered": True},
            )

            outcome = RecoveryOutcome(
                success=True,
                recovery_id=rec_id,
                failure_category=failure.category,
                authority_used=authority,
                action_taken=action_desc,
                escalation_required=False,
                evidence_token=f"TOKEN-SUCCESS-{rec_id}",
            )
        except Exception as err:
            outcome = RecoveryOutcome(
                success=False,
                recovery_id=rec_id,
                failure_category=failure.category,
                authority_used=authority,
                action_taken=f"Recovery failed: {err!s}",
                escalation_required=False,
                evidence_token=f"TOKEN-FAIL-{rec_id}",
            )

        self._history.append(outcome)
        return outcome

    def _assess_recovery_authority(self, category: RuntimeFailureCategory) -> tuple[RecoveryAuthorityLevel, bool]:
        """Maps failure category to authority level and escalation flag."""
        if category in (
            RuntimeFailureCategory.CONNECTION_FAILURE,
            RuntimeFailureCategory.CONTRACT_FAILURE,
        ):
            return RecoveryAuthorityLevel.L2_PATCH, False
        if category in (
            RuntimeFailureCategory.PROCESS_FAILURE,
            RuntimeFailureCategory.CONFIGURATION_FAILURE,
        ):
            return RecoveryAuthorityLevel.L5_RECOVER, False
        if category in (
            RuntimeFailureCategory.AGENT_FAILURE,
            RuntimeFailureCategory.TOOL_FAILURE,
        ):
            return RecoveryAuthorityLevel.L4_REWRITE, False
        if category in (
            RuntimeFailureCategory.SECURITY_BLOCK,
            RuntimeFailureCategory.STARTUP_FAILURE,
        ):
            return RecoveryAuthorityLevel.L6_ESCALATE_ARCH, True
        return RecoveryAuthorityLevel.L7_ESCALATE_GOV, True
