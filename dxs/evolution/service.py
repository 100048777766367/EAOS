from __future__ import annotations

from pathlib import Path

from .capability_discovery import CapabilityDiscovery, DiscoveredCapability
from .evidence import EvolutionEvidence, EvolutionEvidenceService
from .health import HealthCheck, HealthModel
from .migration_readiness import (
    MigrationReadiness,
    MigrationReadinessService,
)


class EvolutionService:
    """Application facade for self-diagnostics and evolution evidence."""

    def __init__(self) -> None:
        self._discovery = CapabilityDiscovery()
        self._readiness = MigrationReadinessService()
        self._evidence = EvolutionEvidenceService()

    def discover(self, root: Path) -> tuple[DiscoveredCapability, ...]:
        """Discover capabilities from the real repository."""
        return self._discovery.discover(root)

    def health(
        self,
        capabilities: tuple[DiscoveredCapability, ...],
    ) -> HealthModel:
        """Build health from discovered repository capabilities."""
        checks = tuple(
            HealthCheck(
                name=capability.name,
                passed=capability.available,
                detail=capability.source,
            )
            for capability in capabilities
        )

        return HealthModel.from_checks(checks)

    def migration_readiness(
        self,
        *,
        health: HealthModel,
        contract_compatible: bool,
        migration_requested: bool = False,
    ) -> MigrationReadiness:
        """Evaluate migration readiness without performing migration."""
        return self._readiness.evaluate(
            repository_healthy=health.status.value == "healthy",
            contract_compatible=contract_compatible,
            migration_requested=migration_requested,
        )

    def evidence(
        self,
        root: Path,
        *,
        capabilities: tuple[DiscoveredCapability, ...],
        health: HealthModel,
        readiness: MigrationReadiness,
    ) -> EvolutionEvidence:
        """Collect immutable evolutionary evidence."""
        return self._evidence.collect(
            root,
            capability_count=len(capabilities),
            healthy=health.status.value == "healthy",
            migration_ready=readiness.ready,
        )
