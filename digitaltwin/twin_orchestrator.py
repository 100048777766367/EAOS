"""Master Digital Twin Orchestrator Engine combining System Graph, Simulation,

Impact Analysis, Consistency, and Delta Checkpoints.
"""

from __future__ import annotations

from digitaltwin.engine.graph_consistency_auditor import (
    ConsistencyReportDTO,
    GraphConsistencyAuditor,
)
from digitaltwin.engine.graph_delta_checkpoint import (
    GraphDeltaCheckpoint,
    GraphDeltaReportDTO,
)
from digitaltwin.engine.impact_analysis_engine import (
    ImpactAnalysisEngine,
    ImpactAnalysisReportDTO,
)
from digitaltwin.engine.system_graph_builder import SystemGraphBuilder
from digitaltwin.models.canonical_graph_model import SystemGraphTopologyDTO
from digitaltwin.models.twin_models import (
    ComponentTwinStateDTO,
    EnterpriseTwinStateDTO,
)
from digitaltwin.replay.twin_replay import TwinEventReplayEngine
from digitaltwin.simulation.twin_simulation import (
    EnterpriseTwinSimulationEngine,
    TwinSimulationResultDTO,
)


class EnterpriseDigitalTwinOrchestrator:
    """Master Orchestrator coordinating System Graph, Impact Analysis, Consistency, Simulation & Replay."""

    def __init__(self) -> None:
        self.simulator = EnterpriseTwinSimulationEngine()
        self.replay = TwinEventReplayEngine()
        self.graph_builder = SystemGraphBuilder()
        self.impact_engine = ImpactAnalysisEngine(self.graph_builder)
        self.consistency_auditor = GraphConsistencyAuditor(self.graph_builder)
        self.delta_checkpoint = GraphDeltaCheckpoint()

    def get_system_graph(self) -> SystemGraphTopologyDTO:
        """Constructs and returns full canonical System Graph topology."""
        return self.graph_builder.build_full_system_graph()

    def analyze_file_impact(self, target_file: str) -> ImpactAnalysisReportDTO:
        """Calculates systemic impact and blast radius for target file change."""
        return self.impact_engine.analyze_impact(target_file)

    def audit_graph_consistency(self) -> ConsistencyReportDTO:
        """Audits graph topology for clean architecture violations and stale nodes."""
        return self.consistency_auditor.audit_graph_consistency()

    def checkpoint_before_change(self, name: str = "BEFORE_MUTATION") -> str:
        """Captures before-change topology snapshot."""
        topology = self.get_system_graph()
        return self.delta_checkpoint.capture_snapshot(name, topology)

    def compare_after_change(self, before_name: str = "BEFORE_MUTATION") -> GraphDeltaReportDTO:
        """Calculates actual graph delta against saved snapshot."""
        after_topology = self.get_system_graph()
        return self.delta_checkpoint.compare_delta(before_name, after_topology)

    def get_current_twin_state(self) -> EnterpriseTwinStateDTO:
        """Construct current Digital Twin state snapshot."""
        graph = self.get_system_graph()
        comps = [
            ComponentTwinStateDTO(
                component_id="api_gateway",
                component_name="FastAPI Gateway",
                health_score=100.0,
            ),
            ComponentTwinStateDTO(
                component_id="system_graph",
                component_name=(f"System Graph ({graph.total_nodes} nodes, {graph.total_edges} edges)"),
                health_score=100.0,
            ),
        ]
        return EnterpriseTwinStateDTO(
            twin_id=graph.twin_id,
            overall_health_score=100.0,
            active_components_count=len(comps),
            components=comps,
        )

    def simulate_change(self, scenario_name: str) -> TwinSimulationResultDTO:
        """Run what-if simulation scenario on digital twin."""
        state = self.get_current_twin_state()
        return self.simulator.run_what_if_simulation(state, scenario_name)
