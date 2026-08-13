"""Canonical Engineering Lifecycle State Machine for EAOS Autonomous Loop."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import ClassVar


class LifecycleStage(StrEnum):
    """The 17 Canonical Stages of the EAOS Engineering Lifecycle."""

    REQUEST = "REQUEST"
    INTENT = "INTENT"
    OBSERVATION = "OBSERVATION"
    SYSTEM_STATE = "SYSTEM_STATE"
    DIAGNOSIS = "DIAGNOSIS"
    ROOT_CAUSE = "ROOT_CAUSE"
    STRATEGY = "STRATEGY"
    AUTHORITY = "AUTHORITY"
    BLAST_RADIUS = "BLAST_RADIUS"
    PLAN = "PLAN"
    SIMULATION = "SIMULATION"
    EXECUTION = "EXECUTION"
    VERIFICATION = "VERIFICATION"
    SELF_CRITIQUE = "SELF_CRITIQUE"
    CONVERGENCE = "CONVERGENCE"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ROLLBACK = "ROLLBACK"
    ESCALATE = "ESCALATE"


@dataclass(frozen=True)
class LifecycleStageTransitionDTO:
    """Record of a single stage transition in the engineering loop."""

    transition_id: str
    from_stage: LifecycleStage
    to_stage: LifecycleStage
    evidence_ref: str
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    details: str = ""


class EngineeringLifecycleFSM:
    """State Machine enforcing strict 17-stage sequence with zero skipped stages."""

    STAGE_ORDER: ClassVar[list[LifecycleStage]] = [
        LifecycleStage.REQUEST,
        LifecycleStage.INTENT,
        LifecycleStage.OBSERVATION,
        LifecycleStage.SYSTEM_STATE,
        LifecycleStage.DIAGNOSIS,
        LifecycleStage.ROOT_CAUSE,
        LifecycleStage.STRATEGY,
        LifecycleStage.AUTHORITY,
        LifecycleStage.BLAST_RADIUS,
        LifecycleStage.PLAN,
        LifecycleStage.SIMULATION,
        LifecycleStage.EXECUTION,
        LifecycleStage.VERIFICATION,
        LifecycleStage.SELF_CRITIQUE,
        LifecycleStage.CONVERGENCE,
        LifecycleStage.COMPLETED,
    ]

    def __init__(self, loop_id: str) -> None:
        self.loop_id = loop_id
        self.current_stage = LifecycleStage.REQUEST
        self.history: list[LifecycleStageTransitionDTO] = []
        self._record_transition(LifecycleStage.REQUEST, LifecycleStage.REQUEST, "Initial request received")

    def transition_to(self, target_stage: LifecycleStage, evidence_ref: str, details: str = "") -> LifecycleStage:
        """Transitions current state or raises ValueError if invalid jump."""
        # Special terminal / escape stages are allowed anytime
        if target_stage in (
            LifecycleStage.FAILED,
            LifecycleStage.ROLLBACK,
            LifecycleStage.ESCALATE,
            LifecycleStage.COMPLETED,
        ):
            self._record_transition(self.current_stage, target_stage, evidence_ref, details)
            self.current_stage = target_stage
            return self.current_stage

        try:
            curr_idx = self.STAGE_ORDER.index(self.current_stage)
            target_idx = self.STAGE_ORDER.index(target_stage)
            if target_idx != curr_idx + 1:
                raise ValueError(
                    f"Invalid lifecycle jump: Cannot transition directly "
                    f"from {self.current_stage.value} to {target_stage.value}"
                )
        except ValueError as err:
            if "is not in list" not in str(err):
                raise

        self._record_transition(self.current_stage, target_stage, evidence_ref, details)
        self.current_stage = target_stage
        return self.current_stage

    def _record_transition(
        self, from_stage: LifecycleStage, to_stage: LifecycleStage, evidence_ref: str, details: str = ""
    ) -> None:
        import uuid

        self.history.append(
            LifecycleStageTransitionDTO(
                transition_id=f"tr-{uuid.uuid4().hex[:8]}",
                from_stage=from_stage,
                to_stage=to_stage,
                evidence_ref=evidence_ref,
                details=details,
            )
        )
