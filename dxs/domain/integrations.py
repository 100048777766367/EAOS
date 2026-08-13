from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IntegrationCheck:
    """Result of an integration environment check."""

    name: str
    path: str
    exists: bool


@dataclass(frozen=True)
class IntegrationReport:
    """Deterministic integration inspection result."""

    checks: tuple[IntegrationCheck, ...]

    @property
    def passed(self) -> bool:
        """Return whether all integration checks passed."""
        return all(check.exists for check in self.checks)
