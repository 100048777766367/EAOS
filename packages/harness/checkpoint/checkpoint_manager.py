from __future__ import annotations

import hashlib
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

"""Real Workspace Checkpoint Snapshot & File Rollback Manager (Rule R39)."""


@dataclass(frozen=True)
class FileSnapshotDTO:
    """Snapshot record for an individual workspace file."""

    rel_path: str
    sha256_hash: str
    backup_path: str


@dataclass(frozen=True)
class WorkspaceCheckpointDTO:
    """Immutable real snapshot of workspace files before execution."""

    checkpoint_id: str
    session_id: str
    turn_id: int
    snapshots: list[FileSnapshotDTO] = field(default_factory=list)


class CheckpointManager:
    """Real File Hashing and Rollback Checkpoint Manager."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root: Final[Path] = (workspace_root or Path.cwd()).resolve()
        self.backup_dir: Final[Path] = self.root / ".memory" / "snapshots"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self._checkpoints: Final[dict[str, WorkspaceCheckpointDTO]] = {}

    def _hash_file(self, path: Path) -> str:
        """Calculates SHA256 content hash for a file."""
        if not path.exists():
            return "EMPTY"
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def create_checkpoint(
        self,
        session_id: str,
        turn_id: int,
        files_to_backup: list[str] | None = None,
    ) -> WorkspaceCheckpointDTO:
        """Captures real SHA256 file hashes and copies backup files."""
        chk_id = f"chk-{session_id}-{turn_id}"
        chk_dir = self.backup_dir / chk_id
        chk_dir.mkdir(parents=True, exist_ok=True)

        snapshots: list[FileSnapshotDTO] = []
        target_files = files_to_backup or ["apps/api/app/routers/chat.py"]

        for rel_p in target_files:
            file_path = self.root / rel_p
            if file_path.exists():
                f_hash = self._hash_file(file_path)
                b_file = chk_dir / file_path.name
                shutil.copy2(file_path, b_file)
                snapshots.append(
                    FileSnapshotDTO(
                        rel_path=rel_p,
                        sha256_hash=f_hash,
                        backup_path=str(b_file),
                    )
                )

        dto = WorkspaceCheckpointDTO(
            checkpoint_id=chk_id,
            session_id=session_id,
            turn_id=turn_id,
            snapshots=snapshots,
        )
        self._checkpoints[chk_id] = dto
        return dto

    def rollback_checkpoint(self, checkpoint_id: str) -> bool:
        """Restores exact original file contents from backup snapshots."""
        dto = self._checkpoints.get(checkpoint_id)
        if not dto:
            return False

        for snap in dto.snapshots:
            backup = Path(snap.backup_path)
            target = self.root / snap.rel_path
            if backup.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(backup, target)

        return True
