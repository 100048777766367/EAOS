from __future__ import annotations

from dxs.adapters.compatibility import CompatibilityAdapter
from dxs.adapters.repository_context import RepositoryContextProvider
from dxs.application.compatibility_service import CompatibilityService
from dxs.application.repository_service import RepositoryApplication
from dxs.evidence.service import EvidenceService
from dxs.health.service import HealthService
from dxs.remediation.service import RemediationService


def create_repository_application() -> RepositoryApplication:
    """Build the DXS repository application composition root."""

    context_provider = RepositoryContextProvider()

    compatibility_service = CompatibilityService(
        checker=CompatibilityAdapter(),
    )

    health_service = HealthService()
    evidence_service = EvidenceService()
    remediation_service = RemediationService()

    return RepositoryApplication(
        context_provider=context_provider,
        compatibility_service=compatibility_service,
        health_service=health_service,
        evidence_service=evidence_service,
        remediation_service=remediation_service,
    )


__all__ = ["create_repository_application"]
