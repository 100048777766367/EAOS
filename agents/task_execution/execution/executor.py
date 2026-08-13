"""Task execution engine."""

from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path

from ..models import AgentTask, TaskState


class TaskExecutor:
    """Execute the task lifecycle without repository mutation."""

    async def execute(
        self,
        task: AgentTask,
        project_root: Path,
    ) -> AsyncIterator[dict[str, object]]:
        """Execute the task and emit lifecycle events."""
        del project_root

        task.transition(TaskState.EXECUTING)
        yield {
            "type": "task_execution_started",
            "task_id": task.task_id,
            "agent_id": task.agent_id,
        }

        # Agent work is deliberately represented as a boundary here.
        # Real coder/architect/security workers are attached later.
        task.result = f"Execution accepted for: {task.request}"

        yield {
            "type": "task_execution_result",
            "task_id": task.task_id,
            "agent_id": task.agent_id,
            "result": task.result,
        }
