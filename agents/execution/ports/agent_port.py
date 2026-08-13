"""Agent execution port."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Protocol

from ..domain.models import TaskRequest


class AgentPort(Protocol):
    """Port implemented by concrete agents."""

    async def execute(
        self,
        request: TaskRequest,
    ) -> AsyncIterator[dict[str, object]]:
        """Execute an agent task."""
        ...
