from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MigrationReadiness:
    """Repository readiness for a contract migration."""

    ready: bool
    blockers: tuple[str, ...]
    evidence: tuple[str, ...]


class MigrationReadinessService:
    """Evaluate migration readiness without executing migration."""

    def evaluate(
        self,
        *,
        repository_healthy: bool,
        contract_compatible: bool,
        migration_requested: bool,
    ) -> MigrationReadiness:
        """Evaluate readiness from observed system conditions."""
        blockers: list[str] = []
        evidence: list[str] = []

        if repository_healthy:
            evidence.append("repository_health=healthy")
        else:
            blockers.append("repository_health_not_healthy")

        if contract_compatible:
            evidence.append("contract_compatibility=compatible")
        else:
            blockers.append("contract_compatibility=not_compatible")

        if migration_requested:
            evidence.append("migration_request=present")
        else:
            evidence.append("migration_request=absent")

        ready = not blockers

        return MigrationReadiness(
            ready=ready,
            blockers=tuple(blockers),
            evidence=tuple(evidence),
        )
