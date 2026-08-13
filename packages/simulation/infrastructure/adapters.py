"""Infrastructure Adapters for Digital Twin Sandbox & Report Storage."""

import time
from typing import Any, override

from packages.simulation.domain.models import (
    BranchEnvironmentType,
    ComparativeResearchReport,
    EmpiricalEvidence,
    EmpiricalMetric,
)
from packages.simulation.domain.ports import (
    DigitalTwinSandboxPort,
    ResearchReportRepositoryPort,
)


class InMemoryDigitalTwinSandboxAdapter(DigitalTwinSandboxPort):
    """Isolated In-Memory Sandbox Adapter for Twin Branching."""

    def __init__(self) -> None:
        self._snapshots: dict[str, dict[str, Any]] = {}
        self._branches: dict[str, dict[str, Any]] = {}

    @override
    def create_snapshot(self, snapshot_id: str, state_data: dict[str, Any]) -> str:
        self._snapshots[snapshot_id] = state_data.copy()
        return snapshot_id

    @override
    def fork_branch(
        self,
        parent_snapshot_id: str,
        branch_id: str,
        branch_type: BranchEnvironmentType,
    ) -> str:
        parent_state = self._snapshots.get(parent_snapshot_id, {})
        self._branches[branch_id] = {
            "type": branch_type,
            "state": parent_state.copy(),
        }
        return branch_id

    @override
    def execute_workload(self, branch_id: str, workload_payload: dict[str, Any]) -> EmpiricalEvidence:
        branch_info = self._branches.get(branch_id, {})
        branch_type = branch_info.get("type", BranchEnvironmentType.BASELINE_ALPHA)

        start_time = time.perf_counter()

        has_mutation = "_mutation" in workload_payload

        if has_mutation:
            mutation = workload_payload["_mutation"]
            time_delay = mutation.get("simulated_delay_ms", 12.0)
            fitness = mutation.get("simulated_fitness", 0.95)
            memory = mutation.get("simulated_memory_mb", 42.0)
            errors = mutation.get("simulated_errors", 0)
        else:
            time_delay = 18.0
            fitness = 0.82
            memory = 55.0
            errors = 0

        time.sleep(time_delay / 1000.0)
        elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)

        return EmpiricalEvidence(
            branch_type=branch_type,
            branch_id=branch_id,
            execution_time_ms=elapsed_ms,
            fitness_score=fitness,
            memory_usage_mb=memory,
            error_count=errors,
            custom_metrics=[EmpiricalMetric(metric_name="Throughput", value=1200.0, unit="req/sec")],
        )


class InMemoryResearchReportRepository(ResearchReportRepositoryPort):
    """Repository Adapter storing research reports in memory."""

    def __init__(self) -> None:
        self._reports: dict[str, ComparativeResearchReport] = {}

    @override
    def save_report(self, report: ComparativeResearchReport) -> ComparativeResearchReport:
        self._reports[report.report_id] = report
        return report

    @override
    def find_report_by_id(self, report_id: str) -> ComparativeResearchReport | None:
        return self._reports.get(report_id)


class InMemorySimulationRepository(ResearchReportRepositoryPort):
    """Repository Adapter storing simulation/research reports in memory (Alias)."""

    def __init__(self) -> None:
        self._reports: dict[str, ComparativeResearchReport] = {}

    @override
    def save_report(self, report: ComparativeResearchReport) -> ComparativeResearchReport:
        self._reports[report.report_id] = report
        return report

    @override
    def find_report_by_id(self, report_id: str) -> ComparativeResearchReport | None:
        return self._reports.get(report_id)
