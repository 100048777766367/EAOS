from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

"""Agent base definitions."""


class AgentRole(StrEnum):
    """Agent roles enum."""

    PLANNER = "PLANNER"
    ARCHITECT = "ARCHITECT"
    SECURITY = "SECURITY"
    CODER = "CODER"
    REVIEWER = "REVIEWER"
    TESTER = "TESTER"
    DEPOPS = "DEPOPS"


@dataclass
class AgentWorkResult:
    """Agent work result DTO."""

    agent_role: AgentRole
    success: bool = True
    summary: str = ""
    details: dict[str, Any] = field(default_factory=dict)
