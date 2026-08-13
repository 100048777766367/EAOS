"""Execution port."""

from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path
from typing import Protocol

from ..models import AgentTask


class ExecutionPort(Protocol):
    """Port implemented by task execution adapters."""

    async def execute(
        self,
        task: AgentTask,
        project_root: Path,
    ) -> AsyncIterator[dict[str, object]]:
        """Execute a task and emit lifecycle events."""
        ...
