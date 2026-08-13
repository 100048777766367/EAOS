from __future__ import annotations

from dxs.ai.adapters import AIRequest
from dxs.ai.policy import (
    AIPolicy,
    PolicyDecision,
    PolicyResult,
)


class AIPolicyService:
    """Application service enforcing the AI policy boundary."""

    def __init__(self, policy: AIPolicy) -> None:
        self._policy = policy

    def evaluate(self, request: AIRequest) -> PolicyResult:
        """Evaluate an AI request without executing it."""
        if not self._policy.enabled:
            return PolicyResult(
                decision=PolicyDecision.DENY,
                reason="AI policy is disabled.",
            )

        if request.capability not in self._policy.allowed_capabilities:
            return PolicyResult(
                decision=PolicyDecision.DENY,
                reason=(f"Capability is not allowed by the active AI policy: {request.capability}"),
            )

        if len(request.prompt) > self._policy.max_prompt_length:
            return PolicyResult(
                decision=PolicyDecision.DENY,
                reason=(f"Prompt exceeds the active maximum length: {self._policy.max_prompt_length}"),
            )

        return PolicyResult(
            decision=PolicyDecision.ALLOW,
            reason="Request is allowed by the active AI policy.",
        )

    def authorize(self, request: AIRequest) -> None:
        """Raise when policy does not permit the request."""
        result = self.evaluate(request)

        if not result.allowed:
            raise PermissionError(result.reason)
