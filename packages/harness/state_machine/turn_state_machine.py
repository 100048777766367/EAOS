from __future__ import annotations

from typing import ClassVar

from packages.harness.domain.states import TurnState

"""Turn State Machine Implementation with Strict Transitions."""


class InvalidStateTransitionError(Exception):
    """Raised when an illegal FSM state transition is attempted."""


class TurnStateMachine:
    """Manages turn lifecycle transitions with validation."""

    VALID_TRANSITIONS: ClassVar[set[tuple[TurnState, TurnState]]] = {
        (TurnState.CREATED, TurnState.RESTORED),
        (TurnState.RESTORED, TurnState.CONTEXT_READY),
        (TurnState.CONTEXT_READY, TurnState.DECIDING),
        (TurnState.DECIDING, TurnState.PROPOSED),
        (TurnState.PROPOSED, TurnState.VALIDATING),
        (TurnState.VALIDATING, TurnState.APPROVED),
        (TurnState.VALIDATING, TurnState.REJECTED),
        (TurnState.APPROVED, TurnState.EXECUTING),
        (TurnState.EXECUTING, TurnState.OBSERVING),
        (TurnState.OBSERVING, TurnState.VERIFYING),
        (TurnState.VERIFYING, TurnState.COMMITTED),
        (TurnState.VERIFYING, TurnState.RECOVERING),
        (TurnState.RECOVERING, TurnState.ROLLED_BACK),
    }

    def __init__(self) -> None:
        self._current_state: TurnState = TurnState.CREATED
        self._checkpoint_active: bool = False

    @property
    def state(self) -> TurnState:
        """Returns current state."""
        return self._current_state

    def transition(self, new_state: TurnState) -> None:
        """Transition only through the canonical state matrix."""
        transition = (self._current_state, new_state)

        if transition not in self.VALID_TRANSITIONS:
            raise InvalidStateTransitionError(f"Illegal transition: {self._current_state.value} -> {new_state.value}")

        self._current_state = new_state

    def transition_to(self, new_state: TurnState) -> None:
        """Alias for transition method."""
        self.transition(new_state)

    def set_checkpoint_active(self, active: bool) -> None:
        """Sets checkpoint active status."""
        self._checkpoint_active = active
