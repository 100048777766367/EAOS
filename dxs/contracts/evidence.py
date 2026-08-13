from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any

from .diagnostics import Diagnostic


@dataclass(frozen=True, slots=True)
class Evidence:
    operation: str
    status: str
    started_at: str
    completed_at: str
    diagnostics: tuple[Diagnostic, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def start(cls, operation: str) -> Evidence:
        now = datetime.now(UTC).isoformat()
        return cls(operation, "running", now, now)

    def complete(self, status: str) -> Evidence:
        return Evidence(
            self.operation,
            status,
            self.started_at,
            datetime.now(UTC).isoformat(),
            self.diagnostics,
            self.metadata,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
