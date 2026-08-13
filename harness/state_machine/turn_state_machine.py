"""Compatibility facade for the canonical EAOS state machine."""

from packages.harness.domain.states import TurnState
from packages.harness.state_machine.turn_state_machine import (
    InvalidStateTransitionError,
    TurnStateMachine,
)

__all__ = [
    "InvalidStateTransitionError",
    "TurnState",
    "TurnStateMachine",
]
