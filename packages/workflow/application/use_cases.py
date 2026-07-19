import uuid
from datetime import UTC, datetime

import structlog
from pydantic import BaseModel

from packages.workflow.domain.models import WorkflowInstance
from packages.workflow.domain.ports import WorkflowRegistryPort

# Cấu hình Structured Logging phục vụ Observability
logger = structlog.get_logger()


class StartWorkflowRequest(BaseModel):
    workflow_id: str


class TransitionWorkflowRequest(BaseModel):
    instance_id: str
    trigger: str


class ExecuteWorkflowUseCase:
    """Application Service quản lý việc khởi tạo và chuyển đổi trạng thái."""

    def __init__(self, registry: WorkflowRegistryPort) -> None:
        self.registry = registry

    def start_workflow(self, request: StartWorkflowRequest) -> WorkflowInstance:
        definition = self.registry.find_definition_by_id(request.workflow_id)
        if not definition:
            raise ValueError(f"Không tìm thấy quy trình: {request.workflow_id}")

        instance_id = f"WFI-{uuid.uuid4().hex[:6].upper()}"
        instance = WorkflowInstance(
            instance_id=instance_id,
            workflow_id=request.workflow_id,
            current_state=definition.initial_state,
            history=[definition.initial_state],
            updated_at=datetime.now(UTC),
        )

        # Ghi nhận vết khởi chạy (Observability)
        logger.info(
            "Workflow instance started",
            workflow_id=request.workflow_id,
            instance_id=instance_id,
            initial_state=definition.initial_state,
        )

        return self.registry.save_instance(instance)

    def transition_workflow(
        self, request: TransitionWorkflowRequest, simulate_stuck: bool = False
    ) -> WorkflowInstance:
        instance = self.registry.find_instance_by_id(request.instance_id)
        if not instance:
            raise ValueError(f"Không thấy phiên chạy: {request.instance_id}")

        definition = self.registry.find_definition_by_id(instance.workflow_id)
        if not definition:
            raise ValueError(f"Không tìm thấy quy trình: {instance.workflow_id}")

        # GIA CỐ: Tự phát hiện Stuck (Mắc kẹt) dựa trên thời gian thực hoặc cờ giả lập
        now = datetime.now(UTC)
        time_elapsed = (now - instance.updated_at).total_seconds()

        # Thiết lập ngưỡng timeout mắc kẹt là 60 giây (hoặc cờ giả lập)
        if time_elapsed > 60.0 or simulate_stuck:
            logger.error(
                "Workflow FSM stuck detected! Activating auto-recovery...",
                instance_id=instance.instance_id,
                time_elapsed=time_elapsed,
            )
            # Tự động cứu hộ chuyển dịch về trạng thái "rejected" / "failed" an toàn
            # Dòng 76: Cứu hộ tự động FSM Stuck
            new_history = [*instance.history, "rejected"]
            recovered_instance = instance.model_copy(
                update={
                    "current_state": "rejected",
                    "history": new_history,
                    "updated_at": now,
                }
            )
            return self.registry.save_instance(recovered_instance)

        current_state_def = None
        for s in definition.states:
            if s.name == instance.current_state:
                current_state_def = s
                break

        if not current_state_def:
            raise ValueError(f"Trạng thái '{instance.current_state}' lỗi.")

        next_state = None
        for t in current_state_def.transitions:
            if t.trigger == request.trigger:
                next_state = t.target
                break

        if not next_state:
            raise ValueError(
                f"Trigger '{request.trigger}' không hợp lệ tại "
                f"trạng thái '{instance.current_state}'."
            )

        # Dòng 107: Chuyển trạng thái FSM thành công
        new_history = [*instance.history, next_state]
        updated_instance = instance.model_copy(
            update={
                "current_state": next_state,
                "history": new_history,
                "updated_at": now,
            }
        )

        # Ghi nhận vết chuyển dịch thành công
        logger.info(
            "Workflow state transitioned",
            instance_id=instance.instance_id,
            old_state=instance.current_state,
            new_state=next_state,
            trigger=request.trigger,
        )

        return self.registry.save_instance(updated_instance)
