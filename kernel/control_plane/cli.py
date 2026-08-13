"""EAOS Control Plane CLI Interface."""

from __future__ import annotations

from pathlib import Path

from kernel.control_plane.authority_engine import AuthorityEngine
from kernel.control_plane.evidence_ledger import EvidenceLedger, TaskEvidenceRecord
from kernel.control_plane.integrity_guard import IntegrityGuard
from kernel.control_plane.state_machine import ControlPlaneState, ControlPlaneStateMachine
from kernel.control_plane.strategy_engine import StrategyEngine
from kernel.control_plane.verification_engine import VerificationEngine


class EAOSControlPlaneCLI:
    """CLI Driver for EAOS Control Plane Operation."""

    def __init__(self, workspace_root: Path | str = ".") -> None:
        self.workspace_root = Path(workspace_root).resolve()
        self.sm = ControlPlaneStateMachine()
        self.authority_engine = AuthorityEngine()
        self.strategy_engine = StrategyEngine()
        self.integrity_guard = IntegrityGuard(self.workspace_root)
        self.verification_engine = VerificationEngine(self.workspace_root)
        self.ledger = EvidenceLedger(self.workspace_root / ".eaos_ledger")

    def run_control_plane_audit(self) -> dict[str, str]:
        """Execute full Control Plane audit of the system."""
        # 1. State: REQUEST -> INTENT
        self.sm.transition_to(ControlPlaneState.INTENT, "Task Audit Initialized")

        # 2. State: INTENT -> INSPECT
        self.sm.transition_to(ControlPlaneState.INSPECT, "Inspecting repository integrity")
        audit_report = self.integrity_guard.audit_integrity()

        # 3. State: INSPECT -> DIAGNOSE
        if audit_report.syntax_error_count >= 20:
            self.sm.transition_to(ControlPlaneState.CORRUPTED, "Mass syntax errors detected")
            root_cause = "Repository corruption detected (>=20 syntax errors)."
            is_corrupted = True
        else:
            self.sm.transition_to(ControlPlaneState.DIAGNOSE, "Auditing causal root causes")
            root_cause = audit_report.rationale
            is_corrupted = False

        # 4. State: DIAGNOSE -> PLAN / RECOVER / ESCALATE
        decision = self.strategy_engine.determine_strategy(
            root_cause=root_cause,
            affected_files_count=len(audit_report.corrupted_files),
            syntax_errors_count=audit_report.syntax_error_count,
            is_corrupted=is_corrupted,
        )

        if decision.strategy.value == "RECOVER":
            self.sm.transition_to(ControlPlaneState.ROLLBACK, "Selecting RECOVER strategy")
        else:
            self.sm.transition_to(ControlPlaneState.PLAN, f"Strategy selected: {decision.strategy.value}")

        # 5. Verification
        verif_report = self.verification_engine.run_adaptive_pipeline("AUDIT")

        # Record Evidence
        rec = TaskEvidenceRecord(
            task_id="AUDIT_001",
            intent="Execute EAOS Control Plane Audit",
            authority_level="L1_DIAGNOSE",
            root_cause=root_cause,
            strategy=decision.strategy.value,
            blast_radius=decision.blast_radius.value,
            affected_files=audit_report.corrupted_files,
            verification_results={"COMPILE": "PASS" if verif_report.overall_passed else "FAIL"},
            decision="CONVERGED" if verif_report.overall_passed else "DEGRADED",
            evidence_text=audit_report.rationale + "\n" + verif_report.summary,
        )
        self.ledger.record_task(rec)

        return {
            "status": "PASS" if verif_report.overall_passed else "FAIL",
            "integrity_state": audit_report.state.value,
            "strategy": decision.strategy.value,
            "blast_radius": decision.blast_radius.value,
            "syntax_errors": str(audit_report.syntax_error_count),
            "summary": verif_report.summary,
        }
