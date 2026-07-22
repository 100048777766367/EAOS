import uuid
from datetime import UTC, datetime

import structlog
from pydantic import BaseModel, Field

from packages.workflow.domain.models import WorkflowInstance
from packages.workflow.domain.ports import WorkflowRegistryPort

logger = structlog.get_logger()


class StartWorkflowRequest(BaseModel):
    workflow_id: str
    initiated_by: str = Field(default="system")
    author: str = Field(default="system")


class TransitionWorkflowRequest(BaseModel):
    instance_id: str
    trigger: str


class ExecuteWorkflowUseCase:
    def __init__(self, registry: WorkflowRegistryPort) -> None:
        self.registry = registry

    def start_workflow(self, request: StartWorkflowRequest) -> WorkflowInstance:
        definition = self.registry.find_definition_by_id(request.workflow_id)
        if not definition:
            raise ValueError(f"Workflow {request.workflow_id} không tồn tại.")

        instance_id = f"WFI-{uuid.uuid4().hex[:6].upper()}"
        initiator = request.initiated_by or request.author
        instance = WorkflowInstance(
            instance_id=instance_id,
            workflow_id=definition.id,
            current_state=definition.initial_state,
            history=[f"Started at {datetime.now(UTC)} by {initiator}"],
        )

        logger.info(
            "Workflow instance started",
            initial_state=definition.initial_state,
            instance_id=instance_id,
            workflow_id=definition.id,
        )
        return self.registry.save_instance(instance)

    def transition_workflow(self, request: TransitionWorkflowRequest, simulate_stuck: bool = False) -> WorkflowInstance:
        instance = self.registry.find_instance_by_id(request.instance_id)
        if not instance:
            raise ValueError(f"Workflow instance {request.instance_id} không tồn tại.")

        definition = self.registry.find_definition_by_id(instance.workflow_id)
        if not definition:
            raise ValueError(f"Workflow definition {instance.workflow_id} không tồn tại.")

        if simulate_stuck:
            stuck_instance = WorkflowInstance(
                instance_id=instance.instance_id,
                workflow_id=instance.workflow_id,
                current_state="STUCK_TIMEOUT_ERROR",
                history=[
                    *instance.history,
                    f"Simulated stuck at {datetime.now(UTC)}. Resilience rescue triggered.",
                ],
            )
            logger.warn(
                "Workflow instance stuck detected",
                instance_id=instance.instance_id,
                state="STUCK_TIMEOUT_ERROR",
            )
            return self.registry.save_instance(stuck_instance)

        current_state_def = None
        for s in definition.states:
            if s.name == instance.current_state:
                current_state_def = s
                break

        if not current_state_def:
            raise ValueError(f"Trạng thái '{instance.current_state}' không hợp lệ.")

        target_state = None
        for t in current_state_def.transitions:
            if t.trigger == request.trigger:
                target_state = t.target
                break

        if not target_state:
            raise ValueError(f"Transition '{request.trigger}' không hợp lệ từ trạng thái '{instance.current_state}'.")

        updated_instance = WorkflowInstance(
            instance_id=instance.instance_id,
            workflow_id=instance.workflow_id,
            current_state=target_state,
            history=[
                *instance.history,
                f"Transitioned to {target_state} via {request.trigger} at {datetime.now(UTC)}",
            ],
        )

        logger.info(
            "Workflow state transitioned",
            instance_id=instance.instance_id,
            old_state=instance.current_state,
            new_state=target_state,
            trigger=request.trigger,
        )
        return self.registry.save_instance(updated_instance)
