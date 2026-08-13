"""Canonical EAOS enterprise agent harness control plane."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from packages.harness.checkpoint.checkpoint_manager import (
    CheckpointManager,
)
from packages.harness.context.context_compiler import ContextCompiler
from packages.harness.domain.actions import (
    ActionIntentDTO,
    ValidatedActionDTO,
)
from packages.harness.domain.states import (
    ActionGateDecision,
    ActionState,
    TurnState,
)
from packages.harness.gates.action_gate import ActionGate
from packages.harness.journal.action_journal import ActionJournal
from packages.harness.recovery.recovery_engine import RecoveryEngine
from packages.harness.state_machine.turn_state_machine import (
    TurnStateMachine,
)
from packages.harness.verification.verification_engine import (
    VerificationEngine,
)


class EAOSAgentHarnessControlPlane:
    """Canonical enterprise harness orchestration boundary.

    The ControlPlane owns composition and lifecycle orchestration.
    Individual domain components retain ownership of their own logic.
    """

    def __init__(
        self,
        workspace_root: Path | None = None,
    ) -> None:
        self.workspace_root = workspace_root.resolve() if workspace_root is not None else Path.cwd().resolve()

        self.fsm = TurnStateMachine()
        self.gate = ActionGate(
            workspace_root=self.workspace_root,
        )
        self.chk_mgr = CheckpointManager(
            workspace_root=self.workspace_root,
        )
        self.context_compiler = ContextCompiler()
        self.journal = ActionJournal()
        self.recovery_engine = RecoveryEngine(
            checkpoint_mgr=self.chk_mgr,
            workspace_root=self.workspace_root,
        )
        self.verification_engine = VerificationEngine(
            root=self.workspace_root,
        )

        self.turn_state = TurnState.CREATED
        self.action_state = ActionState.PROPOSED

    def propose_action(
        self,
        action: ActionIntentDTO,
    ) -> ActionIntentDTO:
        """Register an action proposal."""
        self.turn_state = TurnState.PROPOSED
        self.action_state = ActionState.PROPOSED
        return action

    def validate_action(
        self,
        action: ActionIntentDTO,
    ) -> ValidatedActionDTO:
        """Validate an action through the canonical ActionGate."""
        self.turn_state = TurnState.VALIDATING

        result = self.gate.evaluate_intent(action)

        if result.validated_action is None:
            self.action_state = ActionState.REJECTED
            self.turn_state = TurnState.REJECTED
            raise RuntimeError(result.reason)

        self.action_state = ActionState.PROPOSED

        return ValidatedActionDTO(
            action_id=(getattr(action, "action_id", None) or f"action-{id(action)}"),
            target_uri=str(action.target_uri),
        )

    def decide_action(
        self,
        approved: bool,
        reason: str = "",
    ) -> ActionGateDecision:
        """Record the action-gate decision."""
        decision = ActionGateDecision(
            approved=approved,
            reason=reason,
        )

        if approved:
            self.turn_state = TurnState.APPROVED
            self.action_state = ActionState.APPROVED
        else:
            self.turn_state = TurnState.REJECTED
            self.action_state = ActionState.REJECTED

        return decision

    def begin_execution(self) -> None:
        """Move an approved action into execution."""
        if self.action_state is not ActionState.APPROVED:
            raise RuntimeError("Only an approved action may enter execution.")

        self.turn_state = TurnState.EXECUTING

    def begin_observation(self) -> None:
        """Move execution into observation."""
        if self.turn_state is not TurnState.EXECUTING:
            raise RuntimeError("Observation requires an executing turn.")

        self.turn_state = TurnState.OBSERVING

    def begin_verification(self) -> None:
        """Move observation into verification."""
        if self.turn_state is not TurnState.OBSERVING:
            raise RuntimeError("Verification requires an observed turn.")

        self.turn_state = TurnState.VERIFYING

    def commit(self) -> None:
        """Commit a successfully verified turn."""
        if self.turn_state is not TurnState.VERIFYING:
            raise RuntimeError("Commit requires a verifying turn.")

        self.turn_state = TurnState.COMMITTED

    def recover(self) -> None:
        """Enter recovery."""
        self.turn_state = TurnState.RECOVERING

    def rollback(self) -> None:
        """Mark the current turn as rolled back."""
        self.turn_state = TurnState.ROLLED_BACK

    def run_turn(
        self,
        session_id: str,
        turn_id: int,
        user_id: str,
        task_text: str,
        intent: ActionIntentDTO,
        evidences: list[Any],
        mock_tool_output: str = "",
        exit_code: int = 0,
    ) -> TurnState:
        """Execute the canonical enterprise harness lifecycle."""

        self.journal.log_event(
            session_id=session_id,
            turn_id=turn_id,
            actor=user_id,
            action_name=intent.action_name,
            status="CREATED",
        )

        self.propose_action(intent)

        self.fsm.transition_to(TurnState.RESTORED)
        self.fsm.transition_to(TurnState.CONTEXT_READY)
        self.fsm.transition_to(TurnState.DECIDING)
        self.fsm.transition_to(TurnState.PROPOSED)

        try:
            self.validate_action(intent)

            self.fsm.transition_to(TurnState.VALIDATING)

            self.decide_action(
                approved=True,
                reason="Action allowed by canonical ActionGate.",
            )

            self.fsm.transition_to(TurnState.APPROVED)

            checkpoint = self.chk_mgr.create_checkpoint(
                session_id=session_id,
                turn_id=turn_id,
                files_to_backup=[intent.target_uri],
            )

            self.begin_execution()
            self.fsm.transition_to(TurnState.EXECUTING)

            self.begin_observation()
            self.fsm.transition_to(TurnState.OBSERVING)

            self.begin_verification()
            self.fsm.transition_to(TurnState.VERIFYING)

            verification = self.verification_engine.verify_result(
                action=intent.action_name,
                output=mock_tool_output,
                code=exit_code,
            )

            if not verification["passed"]:
                self.recover()
                self.fsm.transition_to(TurnState.RECOVERING)

                self.chk_mgr.rollback_checkpoint(
                    checkpoint.checkpoint_id,
                )

                self.rollback()
                self.fsm.transition_to(TurnState.ROLLED_BACK)

                self.journal.log_event(
                    session_id=session_id,
                    turn_id=turn_id,
                    actor="EAOS",
                    action_name=intent.action_name,
                    status="ROLLED_BACK",
                )

                return TurnState.ROLLED_BACK

            self.commit()
            self.fsm.transition_to(TurnState.COMMITTED)

            self.journal.log_event(
                session_id=session_id,
                turn_id=turn_id,
                actor="EAOS",
                action_name=intent.action_name,
                status="COMMITTED",
            )

            return TurnState.COMMITTED

        except Exception:
            if self.turn_state not in {
                TurnState.ROLLED_BACK,
                TurnState.COMMITTED,
            }:
                self.turn_state = TurnState.RECOVERING

            raise

    def status(self) -> dict[str, Any]:
        """Return a stable ControlPlane status snapshot."""
        return {
            "workspace_root": str(self.workspace_root),
            "turn_state": self.turn_state.value,
            "action_state": self.action_state.value,
        }
