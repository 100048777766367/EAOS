from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvolutionEvidence:
    """Immutable evidence describing repository evolution state."""

    repository_root: str
    capability_count: int
    healthy: bool
    migration_ready: bool
    files_observed: int


class EvolutionEvidenceService:
    """Produce evidence from actual repository observations."""

    def collect(
        self,
        root: Path,
        *,
        capability_count: int,
        healthy: bool,
        migration_ready: bool,
    ) -> EvolutionEvidence:
        """Collect deterministic filesystem evidence."""
        files_observed = sum(
            1 for path in root.rglob("*") if path.is_file() and ".git" not in path.parts and ".venv" not in path.parts
        )

        return EvolutionEvidence(
            repository_root=str(root),
            capability_count=capability_count,
            healthy=healthy,
            migration_ready=migration_ready,
            files_observed=files_observed,
        )
