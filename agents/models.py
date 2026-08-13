from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

"""Mô hình DTO cho hệ thống Multi-Agent Swarm (AGENTS)."""


class AgentRole(StrEnum):
    """Phân loại vai trò Agent."""

    ARCHITECT = "ARCHITECT"
    CODER = "CODER"
    OPERATOR = "OPERATOR"
    PLANNER = "PLANNER"
    REVIEWER = "REVIEWER"
    SECURITY = "SECURITY"
    TESTER = "TESTER"


@dataclass(frozen=True)
class AgentTask:
    """Nhiệm vụ giao cho Agent Worker."""

    task_id: str
    role: AgentRole
    prompt: str
    parameters: dict[str, str] = field(default_factory=dict)


@dataclass
class AgentExecutionResult:
    """Kết quả thực thi của Agent Worker."""

    task_id: str
    success: bool
    output: str
    proof_hash: str = ""
