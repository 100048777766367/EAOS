"""EAOS Runtime Control Plane — Unified Operational Control & Observation Engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from runtime.automation.bounded_recovery import BoundedRecoveryEngine, RecoveryOutcome
from runtime.inventory.process_control import ProcessManager, ProcessOwnershipDTO, ProcessState
from runtime.policies.failure_taxonomy import RuntimeFailureClassifier, RuntimeFailureRecord
from runtime.state.task_lifecycle import TaskLifecycleFSM, TaskState
from runtime.traces.correlation_engine import CorrelationContext, CorrelationEngine


@dataclass(frozen=True)
class RuntimeSystemGraphNodeDTO:
    """Node representation in the Runtime System Graph."""

    node_id: str
    layer: str  # User, UI, HTTP, WebSocket, Application, Agent, Tool, Process, Mutation, Verification
    status: str
    details: str = ""


@dataclass(frozen=True)
class RuntimeControlStatusDTO:
    """Full operational state summary of EAOS Runtime Control Plane."""

    system_health: str
    active_tasks_count: int
    processes: list[ProcessOwnershipDTO]
    graph_nodes: list[RuntimeSystemGraphNodeDTO]
    last_observation: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class RuntimeControlPlane:
    """Master facade for observing, correlating, controlling, and verifying EAOS runtime execution."""

    def __init__(self) -> None:
        self.correlation = CorrelationEngine()
        self.process_manager = ProcessManager()
        self.failure_classifier = RuntimeFailureClassifier()
        self.recovery_engine = BoundedRecoveryEngine()
        self._active_tasks: dict[str, TaskLifecycleFSM] = {}

    def create_task(
        self,
        user_request_id: str | None = None,
        agent_id: str = "agent-eaos-core",
    ) -> tuple[TaskLifecycleFSM, CorrelationContext]:
        """Creates a new runtime task with stable correlation context and lifecycle FSM."""
        ctx = self.correlation.create_context(user_request_id=user_request_id, agent_id=agent_id)
        fsm = TaskLifecycleFSM(task_id=ctx.task_id)
        self._active_tasks[ctx.task_id] = fsm
        return fsm, ctx

    def get_task_fsm(self, task_id: str) -> TaskLifecycleFSM | None:
        """Returns FSM for active task."""
        return self._active_tasks.get(task_id)

    def transition_task_state(
        self,
        task_id: str,
        target_state: TaskState,
        evidence_token: str,
        metadata: dict[str, Any] | None = None,
    ) -> TaskLifecycleFSM:
        """Transitions task state with evidence token."""
        fsm = self._active_tasks.get(task_id)
        if not fsm:
            fsm = TaskLifecycleFSM(task_id=task_id)
            self._active_tasks[task_id] = fsm

        fsm.transition_to(target_state, evidence_token, metadata)
        return fsm

    def observe_system_graph(self) -> list[RuntimeSystemGraphNodeDTO]:
        """Builds real-time Runtime System Graph representing current operational path."""
        processes = self.process_manager.inspect_all_processes()
        api_proc = next((p for p in processes if p.capability_name == "api_gateway"), None)
        api_status = api_proc.state.value if api_proc else ProcessState.MISSING.value

        return [
            RuntimeSystemGraphNodeDTO(node_id="node-user", layer="User", status="ACTIVE", details="Operator Request"),
            RuntimeSystemGraphNodeDTO(
                node_id="node-ui", layer="UI", status="ACTIVE", details="FastAPI Dashboard / Agent Chat UI"
            ),
            RuntimeSystemGraphNodeDTO(
                node_id="node-http", layer="HTTP/API", status=api_status, details="Port 8000 Gateway"
            ),
            RuntimeSystemGraphNodeDTO(
                node_id="node-ws", layer="WebSocket", status=api_status, details="Route /ws/chat"
            ),
            RuntimeSystemGraphNodeDTO(
                node_id="node-app", layer="Application", status="ACTIVE", details="EAOS Domain Services"
            ),
            RuntimeSystemGraphNodeDTO(
                node_id="node-agent", layer="Agent Orchestrator", status="ACTIVE", details="ChatOrchestrator"
            ),
            RuntimeSystemGraphNodeDTO(
                node_id="node-process", layer="Process", status=api_status, details="Uvicorn / Python PID"
            ),
            RuntimeSystemGraphNodeDTO(
                node_id="node-mutation", layer="Repository Mutation", status="GUARDED", details="L0-L5 Bounded Autonomy"
            ),
            RuntimeSystemGraphNodeDTO(
                node_id="node-verification", layer="Verification", status="ACTIVE", details="EAOS Quality Gates"
            ),
        ]

    def get_control_status(self) -> RuntimeControlStatusDTO:
        """Returns comprehensive operational overview of Runtime Control Plane."""
        processes = self.process_manager.inspect_all_processes()
        graph = self.observe_system_graph()
        all_healthy = all(p.state == ProcessState.HEALTHY for p in processes if p.capability_name == "api_gateway")

        return RuntimeControlStatusDTO(
            system_health="HEALTHY" if all_healthy else "DEGRADED",
            active_tasks_count=len(self._active_tasks),
            processes=processes,
            graph_nodes=graph,
        )

    def handle_runtime_failure(
        self,
        task_id: str,
        exc: Exception | str,
        affected_component: str = "runtime",
    ) -> tuple[RuntimeFailureRecord, RecoveryOutcome]:
        """Classifies failure and executes bounded recovery."""
        failure = self.failure_classifier.classify_exception(exc, affected_component, task_id)
        fsm = self._active_tasks.get(task_id)
        if not fsm:
            fsm = TaskLifecycleFSM(task_id=task_id)
            self._active_tasks[task_id] = fsm

        recovery = self.recovery_engine.attempt_task_recovery(fsm, failure)
        return failure, recovery
