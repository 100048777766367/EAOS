"""Graph Delta Checkpoint Engine comparing expected vs actual topology deltas."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from digitaltwin.models.canonical_graph_model import SystemGraphTopologyDTO


@dataclass(frozen=True)
class GraphDeltaReportDTO:
    """Report comparing expected graph delta vs actual graph delta."""

    checkpoint_id: str
    added_nodes: list[str]
    removed_nodes: list[str]
    added_edges_count: int
    removed_edges_count: int
    exceeds_prediction: bool
    mutation_freeze_required: bool
    details: str
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class GraphDeltaCheckpoint:
    """Manages graph snapshots and calculates topology deltas between system states."""

    def __init__(self) -> None:
        self._snapshots: dict[str, SystemGraphTopologyDTO] = {}

    def capture_snapshot(self, snapshot_name: str, topology: SystemGraphTopologyDTO) -> str:
        """Saves a named topology snapshot."""
        self._snapshots[snapshot_name] = topology
        return snapshot_name

    def get_snapshot(self, snapshot_name: str) -> SystemGraphTopologyDTO | None:
        """Retrieves a saved snapshot."""
        return self._snapshots.get(snapshot_name)

    def list_snapshots(self) -> list[dict[str, str]]:
        """Returns a list of all saved snapshot names and their timestamps."""
        return [{"name": name, "timestamp": topology.timestamp} for name, topology in self._snapshots.items()]

    def delete_snapshot(self, snapshot_name: str) -> bool:
        """Deletes a named snapshot. Returns True if it existed."""
        if snapshot_name in self._snapshots:
            del self._snapshots[snapshot_name]
            return True
        return False

    def compare_delta(
        self,
        before_snapshot_name: str,
        after_topology: SystemGraphTopologyDTO,
        max_allowed_node_delta: int = 10,
    ) -> GraphDeltaReportDTO:
        """Compares before snapshot against after topology and detects unpredicted scope expansion."""
        before = self._snapshots.get(before_snapshot_name)
        chk_id = f"chk-{uuid.uuid4().hex[:8]}"

        if not before:
            return GraphDeltaReportDTO(
                checkpoint_id=chk_id,
                added_nodes=[],
                removed_nodes=[],
                added_edges_count=0,
                removed_edges_count=0,
                exceeds_prediction=False,
                mutation_freeze_required=False,
                details=f"Before snapshot '{before_snapshot_name}' not found",
            )

        before_nodes = {n.node_id for n in before.nodes}
        after_nodes = {n.node_id for n in after_topology.nodes}

        added = list(after_nodes - before_nodes)
        removed = list(before_nodes - after_nodes)

        added_edges = len(after_topology.edges) - len(before.edges)
        exceeds = len(added) > max_allowed_node_delta or len(removed) > max_allowed_node_delta

        return GraphDeltaReportDTO(
            checkpoint_id=chk_id,
            added_nodes=added,
            removed_nodes=removed,
            added_edges_count=max(0, added_edges),
            removed_edges_count=abs(min(0, added_edges)),
            exceeds_prediction=exceeds,
            mutation_freeze_required=exceeds,
            details="Actual blast radius within predicted bounds"
            if not exceeds
            else "Actual graph delta exceeded predicted limits! Freeze mutation required.",
        )
