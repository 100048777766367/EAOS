"""D1.3 Exact Digital Twin graph delta engine."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from digitaltwin.models.canonical_graph_model import SystemGraphTopologyDTO


@dataclass(frozen=True)
class ExactGraphDelta:
    """Exact set-based graph mutation delta."""

    added_nodes: list[str]
    removed_nodes: list[str]
    added_edges: list[tuple[str, str, str]]
    removed_edges: list[tuple[str, str, str]]
    changed_nodes: list[str]
    delta_hash: str
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def added_node_count(self) -> int:
        return len(self.added_nodes)

    @property
    def removed_node_count(self) -> int:
        return len(self.removed_nodes)

    @property
    def added_edge_count(self) -> int:
        return len(self.added_edges)

    @property
    def removed_edge_count(self) -> int:
        return len(self.removed_edges)

    @property
    def total_mutations(self) -> int:
        return (
            self.added_node_count
            + self.removed_node_count
            + self.added_edge_count
            + self.removed_edge_count
            + len(self.changed_nodes)
        )


class ExactGraphDeltaEngine:
    """Calculates exact graph mutation sets."""

    @staticmethod
    def _edge_key(edge: Any) -> tuple[str, str, str]:
        return (
            edge.source_node_id,
            edge.target_node_id,
            edge.edge_type.value,
        )

    @classmethod
    def compare(
        cls,
        before: SystemGraphTopologyDTO,
        after: SystemGraphTopologyDTO,
    ) -> ExactGraphDelta:

        before_nodes = {n.node_id: n for n in before.nodes}
        after_nodes = {n.node_id: n for n in after.nodes}

        added_nodes = sorted(set(after_nodes) - set(before_nodes))
        removed_nodes = sorted(set(before_nodes) - set(after_nodes))

        changed_nodes = [
            node_id
            for node_id in sorted(set(before_nodes) & set(after_nodes))
            if before_nodes[node_id] != after_nodes[node_id]
        ]

        before_edges = {cls._edge_key(edge) for edge in before.edges}

        after_edges = {cls._edge_key(edge) for edge in after.edges}

        added_edges = sorted(after_edges - before_edges)
        removed_edges = sorted(before_edges - after_edges)

        payload = {
            "added_nodes": added_nodes,
            "removed_nodes": removed_nodes,
            "added_edges": added_edges,
            "removed_edges": removed_edges,
            "changed_nodes": changed_nodes,
        }

        delta_json = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
        )

        delta_hash = hashlib.sha256(delta_json.encode("utf-8")).hexdigest()

        return ExactGraphDelta(
            added_nodes=added_nodes,
            removed_nodes=removed_nodes,
            added_edges=added_edges,
            removed_edges=removed_edges,
            changed_nodes=changed_nodes,
            delta_hash=delta_hash,
            metadata={
                "before_twin_id": before.twin_id,
                "after_twin_id": after.twin_id,
            },
        )
