"""Legacy compatibility facade for canonical EAOS Harness states."""

from __future__ import annotations

from packages.harness.domain.actions import SemanticActionType
from packages.harness.domain.states import (
    ActionGateDecision,
    ActionState,
    RecoveryState,
    TurnState,
    VerificationState,
)

__all__ = [
    "ActionGateDecision",
    "ActionState",
    "RecoveryState",
    "SemanticActionType",
    "TurnState",
    "VerificationState",
]
