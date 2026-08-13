from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MigrationRequest:
    """Describe a repository contract migration."""

    current_version: str
    target_version: str


@dataclass(frozen=True)
class MigrationResult:
    """Result of a migration planning operation."""

    current_version: str
    target_version: str
    compatible: bool
    status: str
    reason: str
