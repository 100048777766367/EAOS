from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agents.base import AgentRole

"""Planner worker module."""


@dataclass
class WorkResultDTO:
    """Work result DTO."""

    agent_role: AgentRole
    success: bool
    summary: str


class PlannerWorker:
    """Planner worker implementation."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.workspace_root = workspace_root or Path(".")

    async def execute_work(self, prompt: str, mode: str = "ASK") -> WorkResultDTO:
        """Execute planner work."""
        return WorkResultDTO(
            agent_role=AgentRole.PLANNER,
            success=True,
            summary=f"Plan generated for: {prompt} (mode={mode})",
        )
