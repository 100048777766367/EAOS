from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class PolicyDecision(StrEnum):
    """Decision produced by the AI policy boundary."""

    ALLOW = "allow"
    DENY = "deny"


@dataclass(frozen=True)
class AIPolicy:
    """Provider-neutral AI execution policy."""

    allowed_capabilities: frozenset[str]
    max_prompt_length: int = 10000
    enabled: bool = True

    def __post_init__(self) -> None:
        if self.max_prompt_length <= 0:
            raise ValueError("Maximum prompt length must be greater than zero.")

        normalized = frozenset(capability.strip() for capability in self.allowed_capabilities if capability.strip())

        object.__setattr__(
            self,
            "allowed_capabilities",
            normalized,
        )


@dataclass(frozen=True)
class PolicyResult:
    """Result of an AI policy evaluation."""

    decision: PolicyDecision
    reason: str

    @property
    def allowed(self) -> bool:
        """Return whether policy permits execution."""
        return self.decision is PolicyDecision.ALLOW
