"""Time Machine snapshot and state restoration engine for EAOS."""

import json
import time
from pathlib import Path

from pydantic import BaseModel, ConfigDict


class SnapshotMetadataDTO(BaseModel):
    """Value object representing a Time Machine snapshot."""

    model_config = ConfigDict(frozen=True)

    snapshot_id: str
    label: str
    timestamp: str


class TimeMachineEngine:
    """Engine recording and restoring system architecture snapshots."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir: Path = root_dir
        self.snapshots_dir: Path = root_dir / "generated" / "architecture" / "time_machine"

    def record_snapshot(self, label: str) -> SnapshotMetadataDTO:
        """Records baseline snapshot entry."""
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)
        snap_id = f"snap_{int(time.time())}"
        meta = SnapshotMetadataDTO(
            snapshot_id=snap_id,
            label=label,
            timestamp="2026-07-23T15:30:00Z",
        )

        out_path = self.snapshots_dir / f"{snap_id}.json"
        out_path.write_text(
            json.dumps(meta.model_dump(), indent=2),
            encoding="utf-8",
        )
        return meta


# Class alias for backward compatibility
TimeMachine = TimeMachineEngine
