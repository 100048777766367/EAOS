"""EAOS Control Plane State Machine Engine."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class ControlPlaneState(StrEnum):
    """Execution States of the EAOS Control Plane."""

    REQUEST = "REQUEST"
    INTENT = "INTENT"
    INSPECT = "INSPECT"
    DIAGNOSE = "DIAGNOSE"
    PLAN = "PLAN"
    AUTHORIZE = "AUTHORIZE"
    EXECUTE = "EXECUTE"
    VERIFY = "VERIFY"
    CONVERGE = "CONVERGE"
    ROLLBACK = "ROLLBACK"
    COMPLETE = "COMPLETE"
    CORRUPTED = "CORRUPTED"
    BLOCKED = "BLOCKED"
    ESCALATED = "ESCALATED"
    FAILED = "FAILED"


# Valid State Transition Table
VALID_TRANSITIONS: dict[ControlPlaneState, set[ControlPlaneState]] = {
    ControlPlaneState.REQUEST: {ControlPlaneState.INTENT, ControlPlaneState.BLOCKED, ControlPlaneState.FAILED},
    ControlPlaneState.INTENT: {ControlPlaneState.INSPECT, ControlPlaneState.BLOCKED, ControlPlaneState.FAILED},
    ControlPlaneState.INSPECT: {
        ControlPlaneState.DIAGNOSE,
        ControlPlaneState.CORRUPTED,
        ControlPlaneState.BLOCKED,
        ControlPlaneState.FAILED,
    },
    ControlPlaneState.DIAGNOSE: {
        ControlPlaneState.PLAN,
        ControlPlaneState.CORRUPTED,
        ControlPlaneState.ESCALATED,
        ControlPlaneState.FAILED,
    },
    ControlPlaneState.PLAN: {ControlPlaneState.AUTHORIZE, ControlPlaneState.ESCALATED, ControlPlaneState.FAILED},
    ControlPlaneState.AUTHORIZE: {
        ControlPlaneState.EXECUTE,
        ControlPlaneState.ESCALATED,
        ControlPlaneState.BLOCKED,
        ControlPlaneState.FAILED,
    },
    ControlPlaneState.EXECUTE: {
        ControlPlaneState.VERIFY,
        ControlPlaneState.ROLLBACK,
        ControlPlaneState.CORRUPTED,
        ControlPlaneState.FAILED,
    },
    ControlPlaneState.VERIFY: {
        ControlPlaneState.CONVERGE,
        ControlPlaneState.ROLLBACK,
        ControlPlaneState.FAILED,
    },
    ControlPlaneState.CONVERGE: {ControlPlaneState.COMPLETE, ControlPlaneState.FAILED},
    ControlPlaneState.ROLLBACK: {ControlPlaneState.DIAGNOSE, ControlPlaneState.FAILED, ControlPlaneState.CORRUPTED},
    ControlPlaneState.CORRUPTED: {ControlPlaneState.ROLLBACK, ControlPlaneState.ESCALATED, ControlPlaneState.FAILED},
    ControlPlaneState.ESCALATED: {ControlPlaneState.AUTHORIZE, ControlPlaneState.FAILED},
    ControlPlaneState.BLOCKED: {ControlPlaneState.REQUEST, ControlPlaneState.FAILED},
    ControlPlaneState.COMPLETE: set(),
    ControlPlaneState.FAILED: set(),
}


class StateTransitionRecord(BaseModel):
    """Record of a state transition event."""

    from_state: ControlPlaneState
    to_state: ControlPlaneState
    reason: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class ControlPlaneStateMachine:
    """State Machine Enforcer for EAOS Control Plane."""

    def __init__(self, initial_state: ControlPlaneState = ControlPlaneState.REQUEST) -> None:
        self._current_state = initial_state
        self._history: list[StateTransitionRecord] = []

    @property
    def current_state(self) -> ControlPlaneState:
        return self._current_state

    @property
    def history(self) -> list[StateTransitionRecord]:
        return list(self._history)

    def transition_to(
        self,
        target_state: ControlPlaneState,
        reason: str,
        metadata: dict[str, Any] | None = None,
    ) -> ControlPlaneState:
        """Attempt to transition to a target state enforcing transition validity."""
        allowed = VALID_TRANSITIONS.get(self._current_state, set())
        if target_state not in allowed:
            raise ValueError(
                f"Invalid state transition: '{self._current_state.value}' -> '{target_state.value}'. "
                f"Allowed target states: {[s.value for s in allowed]}"
            )

        record = StateTransitionRecord(
            from_state=self._current_state,
            to_state=target_state,
            reason=reason,
            metadata=metadata or {},
        )
        self._history.append(record)
        self._current_state = target_state
        return self._current_state
