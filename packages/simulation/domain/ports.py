"""Ports for Digital Twin Counterfactual Research Engine."""

from typing import Any, Protocol

from packages.simulation.domain.models import (
    BranchEnvironmentType,
    ComparativeResearchReport,
    EmpiricalEvidence,
)


class DigitalTwinSandboxPort(Protocol):
    """Port for cloning system state and running isolated research workloads."""

    def create_snapshot(self, snapshot_id: str, state_data: dict[str, Any]) -> str:
        """Create a baseline snapshot."""
        ...

    def fork_branch(
        self,
        parent_snapshot_id: str,
        branch_id: str,
        branch_type: BranchEnvironmentType,
    ) -> str:
        """Fork an isolated branch from a parent snapshot."""
        ...

    def execute_workload(self, branch_id: str, workload_payload: dict[str, Any]) -> EmpiricalEvidence:
        """Run empirical workload against a specific branch and collect evidence."""
        ...


class ResearchReportRepositoryPort(Protocol):
    """Port for storing and retrieving empirical research reports."""

    def save_report(self, report: ComparativeResearchReport) -> ComparativeResearchReport:
        """Persist comparative research report."""
        ...

    def find_report_by_id(self, report_id: str) -> ComparativeResearchReport | None:
        """Retrieve report by ID."""
        ...
