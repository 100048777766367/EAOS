from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IdeCheck:
    """Result of an IDE environment check."""

    name: str
    path: str
    exists: bool


@dataclass(frozen=True)
class IdeReport:
    """Deterministic IDE inspection result."""

    checks: tuple[IdeCheck, ...]

    @property
    def passed(self) -> bool:
        """Return whether at least one supported IDE is available."""
        return any(check.exists for check in self.checks)
