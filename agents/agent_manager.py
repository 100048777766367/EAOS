"""Facade Orchestrator managing Swarm 7 Agent Workers, Capability Registry,

Multi-Agent Orchestration, Resource Locking, and Supervision.
"""

from __future__ import annotations

from typing import Any

from digitaltwin.models.canonical_graph_model import BlastRadiusCategory

from agents.concurrency.resource_lock_manager import ResourceLockManager
from agents.orchestration.multi_agent_orchestrator import (
    MultiAgentOrchestrator,
    MultiAgentWorkflowResultDTO,
)
from agents.registry.agent_capability_registry import AgentCapabilityRegistry
from agents.selection.capability_selection_engine import (
    AgentSelectionDecisionDTO,
    CapabilitySelectionEngine,
)
from agents.supervision.agent_supervisor import AgentSupervisor

from .architect.worker import ArchitectWorker
from .automation.dry_run_agent_simulator import DryRunAgentSimulator
from .coder.worker import CoderWorker
from .ledger.quantum_agent_ledger import QuantumAgentLedger
from .models import AgentExecutionResult, AgentRole, AgentTask
from .operator.worker import OperatorWorker
from .planner.worker import PlannerWorker
from .reviewer.worker import ReviewerWorker
from .security.worker import SecurityWorker
from .swarm.swarm_protocol import SwarmProtocol
from .tester.worker import TesterWorker


class AgentManager:
    """Facade hợp nhất điều phối Swarm 7 Agent Workers & Capability Orchestration Engine."""

    def __init__(self) -> None:
        self.architect = ArchitectWorker()
        self.coder = CoderWorker()
        self.operator = OperatorWorker()
        self.planner = PlannerWorker()
        self.reviewer = ReviewerWorker()
        self.security = SecurityWorker()
        self.tester = TesterWorker()
        self.swarm = SwarmProtocol()

        # Capability Orchestration Subsystems
        self.registry = AgentCapabilityRegistry()
        self.selection_engine = CapabilitySelectionEngine(self.registry)
        self.lock_manager = ResourceLockManager()
        self.orchestrator = MultiAgentOrchestrator(self.selection_engine, self.lock_manager)
        self.supervisor = AgentSupervisor()

    def dispatch_task(self, task: AgentTask) -> AgentExecutionResult:
        """Phân phối task cho Agent Worker thích hợp có đóng dấu."""
        output = f"Dispatched task {task.task_id} to {task.role.value}"
        proof = QuantumAgentLedger.generate_agent_proof(task.task_id, {"role": task.role.value, "output": output})
        return AgentExecutionResult(
            task_id=task.task_id,
            success=True,
            output=output,
            proof_hash=proof,
        )

    def select_agents_for_capability(
        self,
        task_id: str,
        intent: str,
        task_type: str,
        required_authority: str,
        blast_radius: BlastRadiusCategory = BlastRadiusCategory.LOCAL,
    ) -> AgentSelectionDecisionDTO:
        """Selects implementer and verifier agents for task."""
        return self.selection_engine.select_agents_for_task(
            task_id=task_id,
            intent=intent,
            task_type=task_type,
            required_authority=required_authority,
            blast_radius=blast_radius,
        )

    def execute_multi_agent_workflow(
        self,
        task_id: str,
        intent: str,
        task_type: str,
        required_authority: str,
        target_files: list[str],
        blast_radius: BlastRadiusCategory = BlastRadiusCategory.LOCAL,
    ) -> MultiAgentWorkflowResultDTO:
        """Runs multi-agent workflow with handoff contracts, resource locks, and verification."""
        return self.orchestrator.orchestrate_task(
            task_id=task_id,
            intent=intent,
            task_type=task_type,
            required_authority=required_authority,
            target_files=target_files,
            blast_radius=blast_radius,
        )

    def simulate_swarm_task(self, role: AgentRole, prompt: str) -> dict[str, Any]:
        """Mô phỏng thực thi task của Swarm."""
        return DryRunAgentSimulator.simulate_task(role.value, prompt)
