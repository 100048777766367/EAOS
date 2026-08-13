from __future__ import annotations

from dataclasses import dataclass, field

"""AI task decomposer."""


@dataclass
class DecomposedPlanDTO:
    """Decomposed plan DTO."""

    subtasks: list[str] = field(default_factory=lambda: ["task1", "task2", "task3"])
    assigned_agents: list[str] = field(default_factory=lambda: ["planner", "architect", "security"])


class AITaskDecomposer:
    """AI task decomposer."""

    def decompose(self, prompt: str) -> DecomposedPlanDTO:
        """Decompose prompt into plan."""
        return DecomposedPlanDTO()
