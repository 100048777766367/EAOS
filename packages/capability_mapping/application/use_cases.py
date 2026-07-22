"""Application use cases for Capability Mapping."""

from packages.capability_mapping.application.dto import (
    AnalyzeCapabilityGapsQuery,
    CapabilityGapReport,
    RegisterCapabilityMappingCommand,
)
from packages.capability_mapping.domain.models import (
    CapabilityMappingAggregate,
    RealizationBinding,
)
from packages.capability_mapping.domain.ports import (
    CapabilityMappingRepositoryPort,
    CodebaseScannerPort,
)


class RegisterCapabilityMappingUseCase:
    def __init__(self, repository: CapabilityMappingRepositoryPort) -> None:
        self._repository = repository

    def execute(self, command: RegisterCapabilityMappingCommand) -> None:
        mapping = CapabilityMappingAggregate(
            capability_id=command.capability_id,
            capability_name=command.capability_name,
            domain_group=command.domain_group,
            maturity_level=command.maturity_level,
        )

        for b in command.bindings:
            mapping.bind_realization(
                RealizationBinding(
                    target_ref=b.target_ref,
                    realization_type=b.realization_type,
                    description=b.description,
                )
            )

        self._repository.save(mapping)


class AnalyzeCapabilityGapsUseCase:
    """Analyzes business capabilities against physical codebase realizations."""

    def __init__(
        self,
        repository: CapabilityMappingRepositoryPort,
        scanner: CodebaseScannerPort,
    ) -> None:
        self._repository = repository
        self._scanner = scanner

    def execute(
        self, query: AnalyzeCapabilityGapsQuery
    ) -> list[CapabilityGapReport]:
        existing_components = self._scanner.scan_existing_components(
            query.workspace_root
        )
        mappings = self._repository.list_all()

        reports: list[CapabilityGapReport] = []

        for m in mappings:
            health = m.calculate_health(existing_components)

            broken = [
                b.target_ref
                for b in m.bindings
                if b.target_ref not in existing_components
            ]

            if health.coverage_percentage == 100.0:
                status = "HEALTHY"
            elif health.coverage_percentage > 0.0:
                status = "DEGRADED"
            else:
                status = "UNREALIZED"

            reports.append(
                CapabilityGapReport(
                    capability_id=m.capability_id,
                    capability_name=m.capability_name,
                    coverage_percentage=health.coverage_percentage,
                    broken_bindings=broken,
                    status=status,
                )
            )

        return reports
