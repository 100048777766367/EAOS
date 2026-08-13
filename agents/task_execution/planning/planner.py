"""Minimal deterministic task planner."""

from __future__ import annotations

from ..models import AgentTask


class TaskPlanner:
    """Create a deterministic initial execution plan."""

    def plan(self, task: AgentTask) -> list[str]:
        """Create and attach the task plan."""
        task.plan = [
            "inspect_request",
            "select_agent",
            "execute_agent",
            "verify_result",
            "record_evidence",
        ]
        return list(task.plan)
