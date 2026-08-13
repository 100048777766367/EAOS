"""Impact Analysis & Blast Radius Engine for EAOS Digital Twin System Graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from digitaltwin.engine.system_graph_builder import SystemGraphBuilder
from digitaltwin.models.canonical_graph_model import BlastRadiusCategory, SystemGraphTopologyDTO


@dataclass(frozen=True)
class ImpactAnalysisReportDTO:
    """Detailed blast radius and systemic impact analysis report."""

    target_file: str
    blast_radius: BlastRadiusCategory
    affected_files_count: int
    required_authority: str
    affected_modules: list[str]
    affected_apis: list[str]
    affected_runtime_processes: list[str]
    crosses_architecture_boundary: bool
    recommended_test_suites: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class ImpactAnalysisEngine:
    """Calculates systemic blast radius, dependency propagation, and risk level for changes."""

    def __init__(self, builder: SystemGraphBuilder | None = None) -> None:
        self.builder = builder or SystemGraphBuilder()

    def analyze_impact(
        self, target_file: str, topology: SystemGraphTopologyDTO | None = None
    ) -> ImpactAnalysisReportDTO:
        """Computes dependency impact and blast radius for a target file."""
        if not topology:
            topology = self.builder.build_full_system_graph()

        clean_target = target_file.replace("\\", "/").strip()
        target_node_id = f"mod:{clean_target}"

        # Find direct and transitive dependent files (importers)
        affected_nodes = self._find_transitive_dependents(target_node_id, topology)
        affected_count = len(affected_nodes)

        # Extract affected modules, APIs, and processes
        affected_modules = [n for n in affected_nodes if n.startswith("mod:")]
        affected_apis = [n for n in affected_nodes if n.startswith("ep:")]
        affected_procs = [n for n in affected_nodes if n.startswith("proc:")]

        # Determine architecture boundary crossing
        crosses_boundary = any(
            "container.py" in clean_target
            or "main.py" in clean_target
            or "ARCHITECTURE_CONSTITUTION" in clean_target
            or "domain" in clean_target
            for clean_target in affected_modules
        )

        # Classify Blast Radius
        if crosses_boundary or "ARCHITECTURE" in clean_target or "CONSTITUTION" in clean_target:
            blast_radius = BlastRadiusCategory.SYSTEMIC
            authority = "L6_OR_L7"
        elif affected_count >= 100:
            blast_radius = BlastRadiusCategory.MASS
            authority = "L5_RECOVER"
        elif affected_count >= 20:
            blast_radius = BlastRadiusCategory.BROAD
            authority = "L4_REWRITE"
        elif affected_count >= 4:
            blast_radius = BlastRadiusCategory.SMALL
            authority = "L3_REFACTOR"
        else:
            blast_radius = BlastRadiusCategory.LOCAL
            authority = "L2_PATCH"

        # Recommends test suites based on blast radius
        test_suites = ["tests/unit/"]
        if blast_radius in (BlastRadiusCategory.BROAD, BlastRadiusCategory.MASS, BlastRadiusCategory.SYSTEMIC):
            test_suites.extend(["tests/integration/", "tests/architecture/", "tests/security/"])
        elif blast_radius == BlastRadiusCategory.SMALL:
            test_suites.append("tests/integration/")

        return ImpactAnalysisReportDTO(
            target_file=clean_target,
            blast_radius=blast_radius,
            affected_files_count=affected_count,
            required_authority=authority,
            affected_modules=affected_modules,
            affected_apis=affected_apis,
            affected_runtime_processes=affected_procs,
            crosses_architecture_boundary=crosses_boundary,
            recommended_test_suites=test_suites,
        )

    def _find_transitive_dependents(self, target_node_id: str, topology: SystemGraphTopologyDTO) -> set[str]:
        """Traverses edge graph to find all nodes that depend on target_node_id."""
        visited: set[str] = {target_node_id}
        queue: list[str] = [target_node_id]

        # Build reverse adjacency list (who imports / depends on node X)
        dependents_map: dict[str, set[str]] = {}
        for edge in topology.edges:
            # edge: source IMPORTS target -> target is imported by source
            target = edge.target_node_id
            source = edge.source_node_id
            if target not in dependents_map:
                dependents_map[target] = set()
            dependents_map[target].add(source)

        while queue:
            curr = queue.pop(0)
            for parent in dependents_map.get(curr, set()):
                if parent not in visited:
                    visited.add(parent)
                    queue.append(parent)

        return visited
