from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

"""Generated Artifacts Lifecycle and Time Machine Manager Engine."""


class TimeMachineSnapshotDTO(BaseModel):
    """Value object representing a Time Machine Architecture Snapshot."""

    model_config = ConfigDict(frozen=True)

    snapshot_id: str = Field(..., description="Snapshot ID e.g. prod_v1")
    file_name: str = Field(..., description="Snapshot file name")
    is_canonical: bool = Field(default=True)


class GeneratedArtifactsManager:
    """Manager auditing time machine snapshots & generated artifacts."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()
        self.gen_dir = self.root / "generated"

    def list_time_machine_snapshots(self) -> list[TimeMachineSnapshotDTO]:
        """List canonical time machine snapshots."""
        tm_dir = self.gen_dir / "architecture" / "time_machine"
        if not tm_dir.exists():
            return []

        snapshots: list[TimeMachineSnapshotDTO] = []
        for f in sorted(tm_dir.glob("*.json")):
            is_gold = "GOLD" in f.name or "baseline" in f.name
            snapshots.append(
                TimeMachineSnapshotDTO(
                    snapshot_id=f.stem,
                    file_name=f.name,
                    is_canonical=is_gold,
                )
            )
        return snapshots

    def purge_invalid_inits(self) -> int:
        """Remove invalid __init__.py files from non-python generated dirs."""
        if not self.gen_dir.exists():
            return 0

        purged = 0
        for init_file in self.gen_dir.rglob("__init__.py"):
            parent = init_file.parent
            py_count = len([f for f in parent.glob("*.py") if f.name != "__init__.py"])
            if py_count == 0:
                init_file.unlink()
                purged += 1
        return purged
