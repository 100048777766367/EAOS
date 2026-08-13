from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class EvidenceStatus(StrEnum):
    """Lifecycle status for diagnostic evidence."""

    OPEN = "open"
    VERIFIED = "verified"
    SUPERSEDED = "superseded"


@dataclass(frozen=True)
class Evidence:
    """Immutable evidence captured during repository diagnostics."""

    key: str
    value: str
    source: str
    status: EvidenceStatus = EvidenceStatus.OPEN
    created_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ValueError("Evidence key must not be empty.")

        if not self.source.strip():
            raise ValueError("Evidence source must not be empty.")
