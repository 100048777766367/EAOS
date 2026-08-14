from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class DiagnosticItem:
    name: str
    status: str
    message: str = ""


@dataclass
class DiagnosticReport:
    timestamp: datetime = field(default_factory=datetime.utcnow)

    items: list[DiagnosticItem] = field(default_factory=list)

    def add(
        self,
        name: str,
        status: str,
        message: str = "",
    ):
        self.items.append(
            DiagnosticItem(
                name=name,
                status=status,
                message=message,
            )
        )

    @property
    def score(self) -> int:
        if not self.items:
            return 0

        passed = sum(1 for item in self.items if item.status == "PASS")

        return int(passed / len(self.items) * 100)
