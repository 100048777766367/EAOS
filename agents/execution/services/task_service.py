"""Application service for agent tasks."""

from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any
from uuid import uuid4

from ..domain.models import TaskRequest
from ..runtime.execution_engine import AgentTaskExecutionEngine


class AgentTaskService:
    """Public application service for task execution."""

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root.resolve()
        self.engine = AgentTaskExecutionEngine(self.project_root)

    async def execute(
        self,
        user_request: str,
        agent_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> AsyncIterator[dict[str, Any]]:
        """Execute an agent task."""
        task_id = "task-" + uuid4().hex[:12]

        request = TaskRequest(
            task_id=task_id,
            user_request=user_request,
            agent_id=agent_id,
            project_root=self.project_root,
            metadata=metadata or {},
        )

        async for event in self.engine.execute(request):
            yield event
