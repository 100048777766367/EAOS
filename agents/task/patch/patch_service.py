"""Repository patch service."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from agents.task.models.task_models import AgentTask


class PatchService:
    """Create patch metadata without applying mutations."""

    def __init__(
        self,
        *,
        allow_apply: bool = False,
    ) -> None:
        self.allow_apply = allow_apply

    def create_patch(
        self,
        project_root: Path,
        task: AgentTask,
    ) -> str:
        """Create a deterministic patch reference."""

        del project_root

        return f"patch-{task.task_id}-{uuid4().hex[:8]}"

    def can_apply(self) -> bool:
        """Return whether patch application is explicitly enabled."""
        return self.allow_apply
