"""Patch and diff management."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..mutation.repository_guard import RepositoryMutationGuard


@dataclass(slots=True)
class PatchResult:
    """Repository patch information."""

    base_revision: str
    diff: str

    @property
    def changed(self) -> bool:
        """Return whether repository changed."""
        return bool(self.diff.strip())


class PatchManager:
    """Create repository diff evidence."""

    def __init__(self) -> None:
        self.guard = RepositoryMutationGuard()

    def capture(self, project_root: Path) -> PatchResult:
        """Capture repository state."""
        revision = self.guard.snapshot(project_root)
        diff = self.guard.diff(project_root)

        return PatchResult(
            base_revision=revision,
            diff=diff,
        )
