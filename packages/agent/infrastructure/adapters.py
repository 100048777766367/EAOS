from packages.agent.domain.models import AIAgent
from packages.agent.domain.ports import AgentRegistryPort


class InMemoryAgentRegistry(AgentRegistryPort):
    """Adapter lưu trữ danh sách AI Agents trong bộ nhớ RAM."""

    def __init__(self) -> None:
        self._store: dict[str, AIAgent] = {}

    def register(self, agent: AIAgent) -> AIAgent:
        self._store[agent.id] = agent
        return agent

    def find_by_id(self, agent_id: str) -> AIAgent | None:
        return self._store.get(agent_id)

    def list_all(self) -> list[AIAgent]:
        return list(self._store.values())

    def update_lifecycle_state(self, agent_id: str, state: str) -> AIAgent:
        agent = self.find_by_id(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} không tồn tại")
        new_history = [*list(agent.lifecycle_history), state]
        updated = agent.model_copy(update={"current_state": state, "lifecycle_history": new_history})
        self.register(updated)
        return updated
