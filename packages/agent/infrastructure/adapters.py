from packages.agent.domain.models import AIAgent
from packages.agent.domain.ports import AgentRegistryPort


class InMemoryAgentRegistry(AgentRegistryPort):
    """Adapter quản lý tiến trình AI Agent có giám sát chuyển dịch trạng thái."""

    def __init__(self) -> None:
        self._store: dict[str, AIAgent] = {}
        # Theo dõi vết thay đổi phục vụ Tracing
        self._transition_audit_log: list[str] = []

    def register(self, agent: AIAgent) -> AIAgent:
        self._store[agent.id] = agent
        return agent

    def find_by_id(self, agent_id: str) -> AIAgent | None:
        return self._store.get(agent_id)

    def list_all(self) -> list[AIAgent]:
        return list(self._store.values())

    def update_lifecycle_state(
        self, agent_id: str, target_state: str
    ) -> AIAgent:
        """Cập nhật trạng thái vòng đời có Tracing Log & Sync Retry."""
        retries = 0
        max_retries = 3
        agent = None

        while retries < max_retries:
            try:
                agent = self.find_by_id(agent_id)
                if not agent:
                    raise ValueError(f"Không tìm thấy Agent: {agent_id}")
                break
            except Exception as e:
                retries += 1
                if retries >= max_retries:
                    raise RuntimeError("Lỗi đồng bộ cấu hình Agent.") from e

        if not agent:
            raise ValueError("Lỗi: Đối tượng Agent rỗng.")

        old_state = agent.current_state
        # GIA CỐ RUF005: Sử dụng toán tử unpacking thay vì cộng list
        new_history = [*agent.lifecycle_history, target_state]
        
        # GIA CỐ E501: Bẻ dòng dictionary để dòng code dưới 88 ký tự
        updated_agent = agent.model_copy(
            update={
                "current_state": target_state,
                "lifecycle_history": new_history,
            }
        )

        # Ghi nhận nhật ký chuyển dịch phục vụ Tracing
        log_msg = (
            f"[Agent Tracing] Agent {agent_id} chuyển trạng thái: "
            f"'{old_state}' ──► '{target_state}'"
        )
        self._transition_audit_log.append(log_msg)
        print(log_msg)

        self.register(updated_agent)
        return updated_agent

    def get_active_agents_count(self) -> int:
        """Đo đạc chỉ số hoạt động (Metrics): Số Agent đang bận rộn."""
        return sum(
            1
            for a in self._store.values()
            if a.current_state != "INITIALIZED"
        )

    def get_transition_logs(self) -> list[str]:
        return self._transition_audit_log