"""Self-diagnostics and evolution services for EAOS DXS."""

from .capability_discovery import CapabilityDiscovery, DiscoveredCapability
from .evidence import EvolutionEvidence, EvolutionEvidenceService
from .health import HealthCheck, HealthModel, HealthStatus
from .migration_readiness import MigrationReadiness, MigrationReadinessService
from .service import EvolutionService

__all__ = [
    "CapabilityDiscovery",
    "DiscoveredCapability",
    "EvolutionEvidence",
    "EvolutionEvidenceService",
    "EvolutionService",
    "HealthCheck",
    "HealthModel",
    "HealthStatus",
    "MigrationReadiness",
    "MigrationReadinessService",
]
