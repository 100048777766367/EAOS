"""Closed-Loop Recovery Engine triggering Rollback and Replanning (Rule R40)."""

from __future__ import annotations

from pathlib import Path
from typing import Final

from harness.checkpoint.checkpoint_manager import CheckpointManager
from harness.domain.failures import FailureReportDTO


class RecoveryEngine:
    """Executes rollback and replan strategy on verification failure."""

    def __init__(
        self,
        checkpoint_mgr: CheckpointManager,
        workspace_root: Path | None = None,
    ) -> None:
        self.root: Final[Path] = (workspace_root or Path.cwd()).resolve()
        self.chk_mgr: Final[CheckpointManager] = checkpoint_mgr

    def execute_recovery(self, failure: FailureReportDTO, checkpoint_id: str) -> bool:
        """Executes rollback if required by failure report."""
        if failure.requires_rollback:
            return self.chk_mgr.rollback_checkpoint(checkpoint_id)
        return True
