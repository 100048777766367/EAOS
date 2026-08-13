"""Action Gate Orchestrator."""

from __future__ import annotations

from packages.harness.domain.actions import ActionIntentDTO
from packages.harness.gates.scope_guard import ScopeGuard
from packages.harness.gates.semantic_classifier import SemanticClassifier
from pydantic import BaseModel, ConfigDict, Field


class ActionProposalDTO(BaseModel):
    """DTO representing action proposal (compatibility alias)."""

    model_config = ConfigDict(frozen=True)
    action_type: str = Field(..., description="Enterprise semantic model field description")
    target: str = Field(..., description="Enterprise semantic model field description")
    payload: str = Field(default="", description="Enterprise semantic model field description")


class ActionGateResultDTO(BaseModel):
    """Result DTO from Action Gate validation."""

    model_config = ConfigDict(frozen=True)
    approved: bool = Field(..., description="Enterprise semantic model field description")
    reason: str = Field(default="", description="Enterprise semantic model field description")


class ActionGate:
    """Integrates scope guard and semantic classifier for action approval."""

    def __init__(
        self,
        scope_guard: ScopeGuard,
        semantic_classifier: SemanticClassifier,
    ) -> None:
        self.scope_guard = scope_guard
        self.semantic_classifier = semantic_classifier

    def evaluate(self, intent: ActionIntentDTO | ActionProposalDTO) -> ActionGateResultDTO:
        """Evaluates action intent against security gates."""
        try:
            self.scope_guard.validate_path(intent.target)
        except Exception as e:
            return ActionGateResultDTO(approved=False, reason=str(e))

        is_safe = self.semantic_classifier.classify(getattr(intent, "action_type", "GENERAL_REPLY"), intent.payload)
        if not is_safe:
            return ActionGateResultDTO(
                approved=False,
                reason="Semantic security violation detected.",
            )

        return ActionGateResultDTO(
            approved=True,
            reason="Action approved successfully.",
        )
