"""Safe Agent Task execution engine."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from pathlib import Path

from agents.task.models.task_models import (
    AgentTask,
    TaskState,
)


class AgentTaskExecutor:
    """Execute an AgentTask without mutating the repository by default."""

    def __init__(
        self,
        *,
        allow_mutation: bool = False,
    ) -> None:
        self.allow_mutation = allow_mutation

    async def execute(
        self,
        task: AgentTask,
        project_root: Path,
    ) -> AsyncIterator[dict[str, object]]:
        """Execute a task and emit lifecycle events."""

        task.transition(TaskState.QUEUED)

        yield {
            "type": "task_lifecycle",
            "state": task.state.value,
            "task_id": task.task_id,
        }

        await asyncio.sleep(0)

        task.transition(TaskState.RUNNING)

        yield {
            "type": "task_lifecycle",
            "state": task.state.value,
            "task_id": task.task_id,
        }

        yield {
            "type": "task_execution_started",
            "task_id": task.task_id,
            "goal": task.goal,
            "project_root": str(project_root),
            "mutation_allowed": self.allow_mutation,
        }
