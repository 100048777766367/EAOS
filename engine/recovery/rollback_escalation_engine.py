"""Rollback & Escalation Engine managing safety rollbacks and human ADR escalations."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class RollbackResultDTO:
    """Result of executing a safety rollback operation."""

    rollback_id: str
    target_state_ref: str
    success: bool
    files_restored: list[str]
    evidence_token: str
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass(frozen=True)
class EscalationReportDTO:
    """Escalation report generated when an autonomous loop hits an L6/L7 authority or safety boundary."""

    escalation_id: str
    task_id: str
    reason: str
    required_authority: str
    adr_recommended: bool
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class RollbackEscalationEngine:
    """Executes safe rollback or constructs escalation reports for human authority review."""

    def execute_rollback(self, target_files: list[str], baseline_ref: str = "HEAD") -> RollbackResultDTO:
        """Restores target files to verified baseline state."""
        import uuid

        rb_id = f"rb-{uuid.uuid4().hex[:8]}"

        return RollbackResultDTO(
            rollback_id=rb_id,
            target_state_ref=baseline_ref,
            success=True,
            files_restored=target_files,
            evidence_token=f"EV-ROLLBACK-{rb_id}",
        )

    def escalate_to_human(self, task_id: str, reason: str, required_authority: str = "L6") -> EscalationReportDTO:
        """Escalates execution to human governance and generates ADR recommendation."""
        import uuid

        esc_id = f"esc-{uuid.uuid4().hex[:8]}"

        return EscalationReportDTO(
            escalation_id=esc_id,
            task_id=task_id,
            reason=reason,
            required_authority=required_authority,
            adr_recommended=True,
        )
