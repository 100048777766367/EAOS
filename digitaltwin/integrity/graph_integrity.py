"""D1.1 Graph Integrity primitives for EAOS Digital Twin."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from digitaltwin.models.canonical_graph_model import (
    GraphEdgeDTO,
    GraphNodeDTO,
    SystemGraphTopologyDTO,
)


@dataclass(frozen=True)
class GraphIntegrityViolation:
    """Single graph integrity violation."""

    code: str
    severity: str
    subject: str
    details: str


@dataclass(frozen=True)
class GraphIntegrityReport:
    """Deterministic graph integrity report."""

    valid: bool
    graph_hash: str
    node_count: int
    edge_count: int
    violations: list[GraphIntegrityViolation] = field(default_factory=list)


class GraphIntegrityValidator:
    """Validates canonical graph invariants."""

    @staticmethod
    def _node_key(node: GraphNodeDTO) -> tuple[str, str, str, str]:
        return (
            node.node_id,
            node.name,
            node.domain.value,
            node.node_type.value,
        )

    @staticmethod
    def _edge_key(edge: GraphEdgeDTO) -> tuple[str, str, str]:
        return (
            edge.source_node_id,
            edge.target_node_id,
            edge.edge_type.value,
        )

    @classmethod
    def canonical_payload(
        cls,
        topology: SystemGraphTopologyDTO,
    ) -> dict[str, Any]:
        """
        Build the deterministic structural representation of a graph.

        IMPORTANT:
        ``last_observed`` is deliberately excluded from the canonical
        identity because it is volatile observation metadata, not graph
        structure. This guarantees that semantically identical graphs
        produce the same hash even when observed at different times.
        """

        nodes = sorted(
            (
                {
                    "node_id": n.node_id,
                    "name": n.name,
                    "domain": n.domain.value,
                    "node_type": n.node_type.value,
                    "provenance": n.provenance.value,
                    "source_of_truth": n.source_of_truth,
                    "authority_level": n.authority_level,
                    "metadata": n.metadata,
                }
                for n in topology.nodes
            ),
            key=lambda x: (
                x["node_id"],
                x["node_type"],
                x["domain"],
                x["name"],
            ),
        )

        edges = sorted(
            (
                {
                    "source_node_id": e.source_node_id,
                    "target_node_id": e.target_node_id,
                    "edge_type": e.edge_type.value,
                    "provenance": e.provenance.value,
                    "evidence_ref": e.evidence_ref,
                    "metadata": e.metadata,
                }
                for e in topology.edges
            ),
            key=lambda x: (
                x["source_node_id"],
                x["target_node_id"],
                x["edge_type"],
                x["provenance"],
                x["evidence_ref"],
            ),
        )

        return {
            "twin_id": topology.twin_id,
            "nodes": nodes,
            "edges": edges,
        }

    @classmethod
    def canonical_json(cls, topology: SystemGraphTopologyDTO) -> str:
        """
        Serialize the structural graph deterministically.

        sort_keys=True guarantees deterministic dictionary ordering.
        separators remove insignificant JSON whitespace.
        ensure_ascii=True gives stable UTF-8/ASCII serialization.
        """

        return json.dumps(
            cls.canonical_payload(topology),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        )

    @classmethod
    def graph_hash(cls, topology: SystemGraphTopologyDTO) -> str:
        """
        Return deterministic SHA-256 hash of graph structure.

        The hash is independent of:
        - node ordering
        - edge ordering
        - dictionary ordering
        - topology timestamp
        - node observation timestamps
        - edge observation timestamps

        The hash changes when structural or authoritative graph content
        changes.
        """

        payload = cls.canonical_json(topology).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    @classmethod
    def validate(
        cls,
        topology: SystemGraphTopologyDTO,
    ) -> GraphIntegrityReport:
        violations: list[GraphIntegrityViolation] = []

        node_ids = [n.node_id for n in topology.nodes]
        node_id_set = set(node_ids)

        # ------------------------------------------------------------
        # 1. Duplicate node IDs
        # ------------------------------------------------------------
        seen_nodes: set[str] = set()

        for node_id in node_ids:
            if node_id in seen_nodes:
                violations.append(
                    GraphIntegrityViolation(
                        code="DUPLICATE_NODE_ID",
                        severity="CRITICAL",
                        subject=node_id,
                        details=f"Duplicate node ID: {node_id}",
                    )
                )

            seen_nodes.add(node_id)

        # ------------------------------------------------------------
        # 2. Empty node IDs
        # ------------------------------------------------------------
        violations.extend(
            GraphIntegrityViolation(
                code="EMPTY_NODE_ID",
                severity="CRITICAL",
                subject="<empty>",
                details="Node ID cannot be empty.",
            )
            for node in topology.nodes
            if not node.node_id.strip()
        )

        # ------------------------------------------------------------
        # 3. Broken references + duplicate edges
        # ------------------------------------------------------------
        edge_keys: set[tuple[str, str, str]] = set()

        for edge in topology.edges:
            if edge.source_node_id not in node_id_set:
                violations.append(
                    GraphIntegrityViolation(
                        code="BROKEN_SOURCE_REF",
                        severity="CRITICAL",
                        subject=edge.source_node_id,
                        details=(f"Edge references missing source node '{edge.source_node_id}'."),
                    )
                )

            if edge.target_node_id not in node_id_set:
                violations.append(
                    GraphIntegrityViolation(
                        code="BROKEN_TARGET_REF",
                        severity="CRITICAL",
                        subject=edge.target_node_id,
                        details=(f"Edge references missing target node '{edge.target_node_id}'."),
                    )
                )

            key = cls._edge_key(edge)

            if key in edge_keys:
                violations.append(
                    GraphIntegrityViolation(
                        code="DUPLICATE_EDGE",
                        severity="CRITICAL",
                        subject="|".join(key),
                        details=f"Duplicate edge: {key}",
                    )
                )

            edge_keys.add(key)

        # ------------------------------------------------------------
        # 4. Metadata count verification
        # ------------------------------------------------------------
        if topology.total_nodes != len(topology.nodes):
            violations.append(
                GraphIntegrityViolation(
                    code="NODE_COUNT_MISMATCH",
                    severity="HIGH",
                    subject=topology.twin_id,
                    details=(f"Declared total_nodes={topology.total_nodes}, actual={len(topology.nodes)}."),
                )
            )

        if topology.total_edges != len(topology.edges):
            violations.append(
                GraphIntegrityViolation(
                    code="EDGE_COUNT_MISMATCH",
                    severity="HIGH",
                    subject=topology.twin_id,
                    details=(f"Declared total_edges={topology.total_edges}, actual={len(topology.edges)}."),
                )
            )

        # ------------------------------------------------------------
        # 5. Provenance summary verification
        # ------------------------------------------------------------
        expected_provenance: dict[str, int] = {}

        for node in topology.nodes:
            key = node.provenance.value
            expected_provenance[key] = expected_provenance.get(key, 0) + 1

        if dict(sorted(expected_provenance.items())) != dict(sorted(topology.provenance_summary.items())):
            violations.append(
                GraphIntegrityViolation(
                    code="PROVENANCE_SUMMARY_MISMATCH",
                    severity="HIGH",
                    subject=topology.twin_id,
                    details=("Declared provenance_summary does not match actual node provenance."),
                )
            )

        return GraphIntegrityReport(
            valid=not violations,
            graph_hash=cls.graph_hash(topology),
            node_count=len(topology.nodes),
            edge_count=len(topology.edges),
            violations=violations,
        )
