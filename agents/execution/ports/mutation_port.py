"""Mutation port."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from ..domain.models import MutationState


class MutationPort(Protocol):
    """Safe repository mutation port."""

    def prepare(self, project_root: Path) -> MutationState:
        """Prepare mutation."""
        ...

    def snapshot(self, project_root: Path) -> str:
        """Create a repository snapshot."""
        ...

    def diff(self, project_root: Path) -> str:
        """Return repository diff."""
        ...
