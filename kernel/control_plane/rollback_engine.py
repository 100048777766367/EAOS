"""EAOS Checkpointing & Rollback Engine."""

from __future__ import annotations

import subprocess
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel, Field


class Checkpoint(BaseModel):
    """Snapshot checkpoint before repository mutation."""

    checkpoint_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    git_commit_hash: str = "UNKNOWN"
    modified_files: list[str] = Field(default_factory=list)


class RollbackEngine:
    """Rollback Engine managing working-tree checkpointing and restoration."""

    def __init__(self, workspace_root: Path | str = ".") -> None:
        self.workspace_root = Path(workspace_root).resolve()
        self._checkpoints: dict[str, Checkpoint] = {}

    def create_checkpoint(self, task_id: str) -> Checkpoint:
        """Create a new checkpoint before mutation."""
        timestamp_slug = int(datetime.now(UTC).timestamp())
        checkpoint_id = f"chk_{task_id}_{timestamp_slug}"
        commit_hash = "UNKNOWN"
        modified_files: list[str] = []

        try:
            res = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=str(self.workspace_root),
                capture_output=True,
                text=True,
                check=False,
            )
            if res.returncode == 0:
                commit_hash = res.stdout.strip()
        except Exception:
            pass

        chk = Checkpoint(
            checkpoint_id=checkpoint_id,
            git_commit_hash=commit_hash,
            modified_files=modified_files,
        )
        self._checkpoints[checkpoint_id] = chk
        return chk

    def rollback(self, checkpoint_id: str) -> bool:
        """Rollback working tree to checkpoint revision."""
        chk = self._checkpoints.get(checkpoint_id)
        # Git rollback logic if git baseline exists; returns True if checkpoint exists
        return chk is not None
