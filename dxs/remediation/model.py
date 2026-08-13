from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RemediationStatus(StrEnum):
    """Lifecycle status for a remediation action."""

    OPEN = "open"
    RESOLVED = "resolved"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class Remediation:
    """Action required to resolve a diagnostic finding."""

    key: str
    description: str
    status: RemediationStatus = RemediationStatus.OPEN

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ValueError("Remediation key must not be empty.")

        if not self.description.strip():
            raise ValueError("Remediation description must not be empty.")
