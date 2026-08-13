from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, computed_field

from packages.harness.gates.scope_guard import ScopeGuard, ScopeViolationError


class ActionGateDecision(StrEnum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    REVIEW = "REVIEW"


class ActionGateResultDTO(BaseModel):
    decision: ActionGateDecision = Field(default=ActionGateDecision.ALLOW)
    validated_action: Any | None = Field(default=None)
    reason: str = Field(default="")
    target_path: str | Path | None = Field(default=None)

    @computed_field
    def rationale(self) -> str:
        return self.reason

    def model_post_init(self, __context: Any) -> None:
        if self.validated_action is None and self.decision == ActionGateDecision.ALLOW:
            self.validated_action = True
        elif self.decision == ActionGateDecision.BLOCK:
            self.validated_action = None


class ActionGate:
    def __init__(self, workspace_root: Path | None = None) -> None:
        self.scope_guard = ScopeGuard(workspace_root)

    def evaluate_intent(self, intent: Any) -> ActionGateResultDTO:
        action_name = str(getattr(intent, "action_name", "") or getattr(intent, "action_type", ""))
        is_destructive = bool(getattr(intent, "is_destructive", False))

        if "reset" in action_name.lower() or is_destructive:
            return ActionGateResultDTO(
                decision=ActionGateDecision.BLOCK,
                validated_action=None,
                reason="Destructive action blocked.",
            )

        target_uri = getattr(intent, "target_uri", None) or getattr(intent, "target", None)
        if target_uri is None:
            return ActionGateResultDTO(
                decision=ActionGateDecision.ALLOW,
                validated_action=intent,
                reason="No target URI provided.",
            )
        try:
            resolved = self.scope_guard.validate_target_path(target_uri)
        except ScopeViolationError as e:
            return ActionGateResultDTO(
                decision=ActionGateDecision.BLOCK,
                validated_action=None,
                reason=str(e),
                target_path=target_uri,
            )
        return ActionGateResultDTO(
            decision=ActionGateDecision.ALLOW,
            validated_action=intent,
            reason="Path within scope.",
            target_path=resolved,
        )
