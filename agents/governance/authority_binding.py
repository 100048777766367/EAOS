"""Authority Binding Model enforcing L0-L7 authority bounds for agent capabilities."""

from __future__ import annotations

from enum import IntEnum, StrEnum
from typing import ClassVar


class AuthorityLevel(IntEnum):
    """L0 through L7 Authority Levels in EAOS Governance."""

    L0_OBSERVE = 0
    L1_DIAGNOSE = 1
    L2_PATCH = 2
    L3_REFACTOR = 3
    L4_REWRITE = 4
    L5_RECOVER = 5
    L6_ARCHITECTURE = 6
    L7_GOVERNANCE = 7


class AuthorityLevelStr(StrEnum):
    L0 = "L0"
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"
    L5 = "L5"
    L6 = "L6"
    L7 = "L7"


class AuthorityViolationError(PermissionError):
    """Raised when an agent capability attempts an operation exceeding its granted authority."""


class AuthorityBindingModel:
    """Enforces governance authority bounds for specialized agents and capabilities."""

    AUTHORITY_MAP: ClassVar[dict[str, AuthorityLevel]] = {
        "L0": AuthorityLevel.L0_OBSERVE,
        "L1": AuthorityLevel.L1_DIAGNOSE,
        "L2": AuthorityLevel.L2_PATCH,
        "L3": AuthorityLevel.L3_REFACTOR,
        "L4": AuthorityLevel.L4_REWRITE,
        "L5": AuthorityLevel.L5_RECOVER,
        "L6": AuthorityLevel.L6_ARCHITECTURE,
        "L7": AuthorityLevel.L7_GOVERNANCE,
    }

    @classmethod
    def parse_level(cls, level_str: str) -> AuthorityLevel:
        """Parses authority level string (e.g. 'L2' or 'L2_PATCH') into AuthorityLevel enum."""
        clean = level_str.split("_")[0].upper().strip()
        return cls.AUTHORITY_MAP.get(clean, AuthorityLevel.L0_OBSERVE)

    @classmethod
    def is_authorized(cls, agent_max_level: str, task_required_level: str) -> bool:
        """Checks if agent max authority is sufficient for required task authority."""
        agent_level = cls.parse_level(agent_max_level)
        required_level = cls.parse_level(task_required_level)

        # L6 and L7 require explicit human approval and cannot be authorized autonomously
        if required_level >= AuthorityLevel.L6_ARCHITECTURE:
            return False

        return agent_level >= required_level

    @classmethod
    def validate_execution(cls, agent_id: str, agent_max_level: str, required_level: str) -> None:
        """Validates execution or raises AuthorityViolationError."""
        req_enum = cls.parse_level(required_level)

        if req_enum >= AuthorityLevel.L6_ARCHITECTURE:
            raise AuthorityViolationError(
                f"Agent '{agent_id}' execution denied: "
                f"Required authority '{required_level}' is L6/L7 "
                "and requires human ADR approval."
            )

        if not cls.is_authorized(agent_max_level, required_level):
            raise AuthorityViolationError(
                f"Agent '{agent_id}' (Max: {agent_max_level}) unauthorized for task requiring '{required_level}'."
            )
