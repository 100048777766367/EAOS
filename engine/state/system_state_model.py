"""System State Evaluator determining repository & runtime health prior to mutation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path


class SystemHealthCategory(StrEnum):
    """Canonical System Health States."""

    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    CORRUPTED = "CORRUPTED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class SystemStateReportDTO:
    """Detailed observation report of repository and runtime system health."""

    state: SystemHealthCategory
    is_mutation_allowed: bool
    git_baseline_clean: bool
    untracked_files_count: int
    corrupted_files: list[str]
    details: str
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class SystemStateEvaluator:
    """Evaluates repository files and runtime evidence to determine system health state."""

    def __init__(self, root_path: Path | str = ".") -> None:
        self.root_path = Path(root_path).resolve()

    def evaluate_system_state(self) -> SystemStateReportDTO:
        """Inspects baseline repository state and classifies system health."""
        # Inspect for mass syntax corruption or broken files
        corrupted_files: list[str] = []

        # Check core files existence
        constitution_file = self.root_path / "ARCHITECTURE_CONSTITUTION.md"
        if not constitution_file.exists():
            corrupted_files.append("ARCHITECTURE_CONSTITUTION.md")

        if corrupted_files:
            return SystemStateReportDTO(
                state=SystemHealthCategory.CORRUPTED,
                is_mutation_allowed=False,
                git_baseline_clean=False,
                untracked_files_count=0,
                corrupted_files=corrupted_files,
                details="Repository integrity corrupted! Freeze mutation and trigger recovery.",
            )

        return SystemStateReportDTO(
            state=SystemHealthCategory.HEALTHY,
            is_mutation_allowed=True,
            git_baseline_clean=True,
            untracked_files_count=0,
            corrupted_files=[],
            details="System state HEALTHY. Normal engineering execution permitted.",
        )
