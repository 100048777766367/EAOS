from pydantic import BaseModel

from packages.agent.domain.models import AIAgent
from packages.agent.domain.ports import AgentRegistryPort


class TransitionLifecycleRequest(BaseModel):
    agent_id: str
    target_state: str


class ExecuteAgentLifecycleUseCase:
    """Application Service điều phối sự chuyển đổi vòng đời của Agent."""

    def __init__(self, registry: AgentRegistryPort) -> None:
        self.registry = registry

    def transition_state(self, request: TransitionLifecycleRequest) -> AIAgent:
        agent = self.registry.find_by_id(request.agent_id)
        if not agent:
            raise ValueError(f"Không tìm thấy Agent: {request.agent_id}")

        # Định nghĩa các trạng thái hợp chuẩn trong Hiến pháp
        VALID_STATES = {
            "INITIALIZED",
            "PLANNING",
            "EXECUTING",
            "REFLECTING",
            "COMPLETED",
            "FAILED",
        }
        target = request.target_state.upper()
        if target not in VALID_STATES:
            raise ValueError(f"Trạng thái '{target}' không hợp lệ.")
        # Sửa lỗi RUF005 bằng unpacking
        new_history = [*agent.lifecycle_history, target]
        updated_agent = agent.model_copy(
            update={"current_state": target, "lifecycle_history": new_history}
        )

        return self.registry.register(updated_agent)
