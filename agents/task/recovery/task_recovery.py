"""Agent Task recovery."""

from __future__ import annotations

from agents.task.models.task_models import (
    AgentTask,
    TaskState,
)


class TaskRecovery:
    """Recover failed tasks into a controlled lifecycle state."""

    def recover(self, task: AgentTask) -> None:
        """Move a task into recovery."""
        task.transition(TaskState.RECOVERING)

    def fail(self, task: AgentTask) -> None:
        """Move a task into failed state."""
        task.transition(TaskState.FAILED)
