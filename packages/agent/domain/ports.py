from typing import Protocol

from packages.agent.domain.models import AIAgent


class AgentRegistryPort(Protocol):
    """Port định nghĩa các hành vi quản lý danh sách AI Agents hoạt động."""

    def register(self, agent: AIAgent) -> AIAgent: ...

    def find_by_id(self, agent_id: str) -> AIAgent | None: ...

    def list_all(self) -> list[AIAgent]: ...