from pydantic import BaseModel

from packages.agent.domain.models import AIAgent
from packages.agent.domain.ports import AgentRegistryPort


class TransitionLifecycleRequest(BaseModel):
    agent_id: str
    target_state: str # PLANNING, EXECUTING, COMPLETED, FAILED

class ExecuteAgentLifecycleUseCase:
    """Application Service quáº£n lÃ½ cháº·t cháº½ vÃ²ng Ä‘á»i thá»±c thi cá»§a cÃ¡c AI Agents."""
    def __init__(self, registry: AgentRegistryPort) -> None:
        self.registry = registry

    def transition_state(self, request: TransitionLifecycleRequest) -> AIAgent:
        return self.registry.update_lifecycle_state(request.agent_id, request.target_state)

