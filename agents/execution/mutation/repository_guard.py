"""Repository mutation guard."""

from __future__ import annotations

import subprocess
from pathlib import Path

from ..domain.models import MutationState


class RepositoryMutationGuard:
    """Protect repository mutation operations."""

    def prepare(self, project_root: Path) -> MutationState:
        """Validate repository root."""
        if not project_root.exists():
            raise FileNotFoundError(project_root)

        if not (project_root / ".eaos").exists():
            raise RuntimeError("EAOS governance directory is missing.")

        return MutationState.PREPARED

    def snapshot(self, project_root: Path) -> str:
        """Return current git HEAD when available."""
        process = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )

        if process.returncode != 0:
            return "NO_GIT_HEAD"

        return process.stdout.strip()

    def diff(self, project_root: Path) -> str:
        """Return current repository diff."""
        process = subprocess.run(
            ["git", "diff", "--"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )

        return process.stdout
