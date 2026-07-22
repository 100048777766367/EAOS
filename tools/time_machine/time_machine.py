import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from tools.metrics.architecture_metrics_calculator import (
    ArchitectureMetricsCalculator,
)
from tools.validate.architecture_validator import ArchitectureValidator


class ArchitectureTimeMachine:
    """Cỗ máy thời gian tự trị lưu vết và đối chiếu lịch sử tiến hóa kiến trúc."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.time_machine_dir = root_dir / "generated" / "architecture" / "time_machine"
        self.time_machine_dir.mkdir(parents=True, exist_ok=True)

    def record_snapshot(self, snapshot_id: str) -> dict[str, Any]:
        """Ghi nhận và chụp lại (Snapshot) trạng thái kiến trúc hiện tại."""
        validator = ArchitectureValidator(self.root_dir)
        validator.run_all_checks()

        metrics_calc = ArchitectureMetricsCalculator(self.root_dir)
        metrics_calc.calculate_all()

        snapshot_data = {
            "snapshot_id": snapshot_id,
            "timestamp": datetime.now(UTC).isoformat(),
            "architecture_score": metrics_calc.architecture_score,
            "active_packages": list(metrics_calc.metrics.keys()),
            "violations": validator.violations,
            "metrics": metrics_calc.metrics,
        }

        file_name = f"snapshot_{snapshot_id}.json"
        file_path = self.time_machine_dir / file_name

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(snapshot_data, f, indent=2, ensure_ascii=False)

        return snapshot_data

    def list_snapshots(self) -> list[dict[str, Any]]:
        """Liệt kê toàn bộ lịch sử các Snapshot đã chụp."""
        snapshots = []
        for file in self.time_machine_dir.glob("snapshot_*.json"):
            try:
                with open(file, encoding="utf-8") as f:
                    snapshots.append(json.load(f))
            except Exception:
                continue
        return sorted(snapshots, key=lambda x: x["timestamp"])

    def compare_snapshots(self, id_a: str, id_b: str) -> dict[str, Any]:
        """Đối chiếu và chẩn đoán sự khác biệt giữa hai Snapshot."""
        file_a = self.time_machine_dir / f"snapshot_{id_a}.json"
        file_b = self.time_machine_dir / f"snapshot_{id_b}.json"

        if not file_a.exists() or not file_b.exists():
            raise ValueError("Một hoặc cả hai mã Snapshot không tồn tại.")

        with open(file_a, encoding="utf-8") as f:
            snap_a = json.load(f)
        with open(file_b, encoding="utf-8") as f:
            snap_b = json.load(f)

        score_diff = snap_b["architecture_score"] - snap_a["architecture_score"]

        pkgs_a = set(snap_a["active_packages"])
        pkgs_b = set(snap_b["active_packages"])
        added_pkgs = list(pkgs_b - pkgs_a)
        removed_pkgs = list(pkgs_a - pkgs_b)

        v_a = set(snap_a["violations"])
        v_b = set(snap_b["violations"])
        new_violations = list(v_b - v_a)
        resolved_violations = list(v_a - v_b)

        return {
            "snapshot_a": id_a,
            "snapshot_b": id_b,
            "score_diff": score_diff,
            "added_packages": added_pkgs,
            "removed_packages": removed_pkgs,
            "new_violations": new_violations,
            "resolved_violations": resolved_violations,
        }
