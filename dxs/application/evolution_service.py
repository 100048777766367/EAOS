from __future__ import annotations

from dataclasses import dataclass

from dxs.contracts.evolution import VersionedContract
from dxs.contracts.versioning import ContractVersion
from dxs.domain.compatibility_matrix import CompatibilityMatrix
from dxs.domain.deprecation import (
    DeprecationPolicy,
    DeprecationStatus,
)
from dxs.domain.migration_plan import (
    MigrationPlan,
    MigrationPlanner,
)


@dataclass(frozen=True, slots=True)
class EvolutionAssessment:
    """Immutable assessment of one contract evolution transition."""

    current: VersionedContract
    target: VersionedContract
    compatible: bool
    deprecation_status: DeprecationStatus
    migration: MigrationPlan


class EvolutionService:
    """Application service for deterministic contract evolution."""

    def __init__(
        self,
        compatibility: CompatibilityMatrix | None = None,
        deprecation: DeprecationPolicy | None = None,
        migration: MigrationPlanner | None = None,
    ) -> None:
        self._compatibility = compatibility or CompatibilityMatrix()
        self._deprecation = deprecation or DeprecationPolicy()
        self._migration = migration or MigrationPlanner()

    def assess(
        self,
        current: VersionedContract,
        target: VersionedContract,
    ) -> EvolutionAssessment:
        """Assess compatibility, lifecycle, and migration readiness."""

        compatible = self._compatibility.is_compatible(
            current.version,
            target.version,
        )

        status = self._deprecation.status(
            current.name,
            current.version,
        )

        plan = self._migration.plan(
            current=current.version,
            target=target.version,
            compatible=compatible,
        )

        return EvolutionAssessment(
            current=current,
            target=target,
            compatible=compatible,
            deprecation_status=status,
            migration=plan,
        )

    def compatible(
        self,
        current: ContractVersion,
        target: ContractVersion,
    ) -> bool:
        """Return compatibility for two versions."""

        return self._compatibility.is_compatible(
            current,
            target,
        )


__all__ = [
    "EvolutionAssessment",
    "EvolutionService",
]
