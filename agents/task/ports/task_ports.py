"""Ports for Agent Task execution."""

from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path
from typing import Protocol

from agents.task.models.task_models import (
    AgentTask,
    TaskResult,
)


class TaskExecutionPort(Protocol):
    """Port implemented by task execution engines."""

    async def execute(
        self,
        task: AgentTask,
        project_root: Path,
    ) -> AsyncIterator[dict[str, object]]:
        """Execute a task and stream events."""
        ...


class TaskPatchPort(Protocol):
    """Port for repository patch operations."""

    def create_patch(
        self,
        project_root: Path,
        task: AgentTask,
    ) -> str:
        """Create a patch identifier."""
        ...


class EvidencePort(Protocol):
    """Port for task evidence persistence."""

    def write(
        self,
        task: AgentTask,
        result: TaskResult,
    ) -> str:
        """Persist task evidence."""
        ...
