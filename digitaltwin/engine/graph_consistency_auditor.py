"""Graph Consistency Auditor evaluating architecture rules and graph health."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from digitaltwin.engine.system_graph_builder import SystemGraphBuilder
from digitaltwin.models.canonical_graph_model import (
    GraphEdgeType,
    SystemGraphTopologyDTO,
)


@dataclass(frozen=True)
class ConsistencyViolationDTO:
    """Single consistency or architecture boundary violation."""

    violation_id: str
    category: str  # ORPHAN_NODE, BROKEN_REF, ARCHITECTURE_VIOLATION, STALE_RUNTIME, CIRCULAR_DEPENDENCY
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    node_id: str
    details: str


@dataclass(frozen=True)
class ConsistencyReportDTO:
    """Overall Graph Consistency Audit Report."""

    is_consistent: bool
    total_violations_count: int
    critical_count: int
    violations: list[ConsistencyViolationDTO]
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class GraphConsistencyAuditor:
    """Audits system graph topology against clean architecture rules and operational integrity."""

    def __init__(self, builder: SystemGraphBuilder | None = None) -> None:
        self.builder = builder or SystemGraphBuilder()

    def audit_graph_consistency(self, topology: SystemGraphTopologyDTO | None = None) -> ConsistencyReportDTO:
        """Runs full suite of graph consistency checks."""
        if not topology:
            topology = self.builder.build_full_system_graph()

        violations: list[ConsistencyViolationDTO] = []
        node_ids = {n.node_id for n in topology.nodes}

        # 1. Check Broken References (edges pointing to unknown source nodes)
        for edge in topology.edges:
            if edge.source_node_id not in node_ids:
                violations.append(
                    ConsistencyViolationDTO(
                        violation_id=f"viol-ref-{len(violations)}",
                        category="BROKEN_REF",
                        severity="HIGH",
                        node_id=edge.source_node_id,
                        details=(f"Edge source node '{edge.source_node_id}' missing in node graph"),
                    )
                )

        # 2. Check Architecture Boundary Violations (Clean/Hexagonal Architecture)
        # Domain modules MUST NOT directly import Infrastructure/Adapters
        for edge in topology.edges:
            if "/domain/" in edge.source_node_id and (
                "/infrastructure/" in edge.target_node_id or "/adapters/" in edge.target_node_id
            ):
                violations.append(
                    ConsistencyViolationDTO(
                        violation_id=f"viol-arch-{len(violations)}",
                        category="ARCHITECTURE_VIOLATION",
                        severity="CRITICAL",
                        node_id=edge.source_node_id,
                        details=(
                            "Clean Architecture Violation: "
                            f"Domain '{edge.source_node_id}' directly imports "
                            f"Infrastructure '{edge.target_node_id}'"
                        ),
                    )
                )

        # 3. Check Stale Runtime Mappings
        for node in topology.nodes:
            if node.domain.value == "RUNTIME" and node.provenance.value in ("STALE", "UNKNOWN"):
                violations.append(
                    ConsistencyViolationDTO(
                        violation_id=f"viol-rt-{len(violations)}",
                        category="STALE_RUNTIME",
                        severity="MEDIUM",
                        node_id=node.node_id,
                        details=(f"Runtime process node '{node.name}' is in {node.provenance.value} state"),
                    )
                )

        # 4. Check Orphan Nodes (no edges at all — not imported and imports nothing)
        connected_nodes: set[str] = set()
        for edge in topology.edges:
            connected_nodes.add(edge.source_node_id)
            connected_nodes.add(edge.target_node_id)

        for node in topology.nodes:
            if node.node_id not in connected_nodes and node.domain.value not in ("GOVERNANCE", "RUNTIME"):
                violations.append(
                    ConsistencyViolationDTO(
                        violation_id=f"viol-orphan-{len(violations)}",
                        category="ORPHAN_NODE",
                        severity="LOW",
                        node_id=node.node_id,
                        details=(f"Module '{node.name}' has no import edges (isolated from system graph)"),
                    )
                )

        # 5. Circular Dependency Detection via DFS on IMPORTS edges
        import_edges: dict[str, list[str]] = {}
        for edge in topology.edges:
            if edge.edge_type == GraphEdgeType.IMPORTS:
                if edge.source_node_id not in import_edges:
                    import_edges[edge.source_node_id] = []
                import_edges[edge.source_node_id].append(edge.target_node_id)

        cycles = self._detect_cycles(import_edges)
        for cycle_path in cycles:
            violations.append(
                ConsistencyViolationDTO(
                    violation_id=f"viol-cycle-{len(violations)}",
                    category="CIRCULAR_DEPENDENCY",
                    severity="HIGH",
                    node_id=cycle_path[0],
                    details=f"Circular import detected: {' → '.join(cycle_path)}",
                )
            )

        critical_count = sum(1 for v in violations if v.severity == "CRITICAL")
        return ConsistencyReportDTO(
            is_consistent=(critical_count == 0),
            total_violations_count=len(violations),
            critical_count=critical_count,
            violations=violations,
        )

    def _detect_cycles(self, adjacency: dict[str, list[str]]) -> list[list[str]]:
        """Detects circular dependencies using DFS with path tracking. Returns list of cycle paths."""
        visited: set[str] = set()
        rec_stack: set[str] = set()
        cycles: list[list[str]] = []

        def dfs(node: str, path: list[str]) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbour in adjacency.get(node, []):
                if neighbour not in visited:
                    dfs(neighbour, path)
                elif neighbour in rec_stack:
                    # Found cycle — extract cycle subpath
                    cycle_start = path.index(neighbour)
                    cycle = [*path[cycle_start:], neighbour]
                    if len(cycles) < 20:  # cap to avoid overwhelming report
                        cycles.append(cycle)

            path.pop()
            rec_stack.discard(node)

        for node in list(adjacency.keys()):
            if node not in visited:
                dfs(node, [])

        return cycles
