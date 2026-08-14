from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GovernanceDecision:
    allowed: bool
    rule: str
    reason: str


__all__ = ["GovernanceDecision"]
