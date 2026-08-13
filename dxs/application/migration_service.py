from __future__ import annotations

from dxs.application.compatibility_service import CompatibilityService
from dxs.contracts.versioning import ContractVersion
from dxs.domain.migration import MigrationRequest, MigrationResult


class MigrationService:
    """Application service for contract migration planning."""

    def __init__(self, compatibility_service: CompatibilityService) -> None:
        self._compatibility_service = compatibility_service

    def plan(
        self,
        request: MigrationRequest,
    ) -> MigrationResult:
        current = ContractVersion.parse(request.current_version)
        target = ContractVersion.parse(request.target_version)

        result = self._compatibility_service.check(
            current=current,
            target=target,
        )

        if not result.compatible:
            return MigrationResult(
                current_version=str(current),
                target_version=str(target),
                compatible=False,
                status="BLOCKED",
                reason=result.reason,
            )

        status = "NOOP" if current == target else "READY"

        return MigrationResult(
            current_version=str(current),
            target_version=str(target),
            compatible=True,
            status=status,
            reason=result.reason,
        )


__all__ = ["MigrationService"]
