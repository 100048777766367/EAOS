from __future__ import annotations

from dataclasses import dataclass

from ai.models.model_provider import AIProviderType

"""FinOps model router."""


@dataclass
class RouteDecisionDTO:
    """Route decision DTO."""

    selected_provider: AIProviderType = AIProviderType.GROQ


class FinOpsModelRouter:
    """FinOps model router."""

    def route_task(self, task_complexity: str = "medium") -> RouteDecisionDTO:
        """Route task based on complexity."""
        return RouteDecisionDTO(selected_provider=AIProviderType.GROQ)
