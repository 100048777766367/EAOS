"""Unit tests for the Capability Mapping context."""

from pathlib import Path

from packages.capability_mapping.application.dto import (
    AnalyzeCapabilityGapsQuery,
    BindingDTO,
    RegisterCapabilityMappingCommand,
)
from packages.capability_mapping.application.use_cases import (
    AnalyzeCapabilityGapsUseCase,
    RegisterCapabilityMappingUseCase,
)
from packages.capability_mapping.domain.models import (
    CapabilityMaturityLevel,
    RealizationType,
)
from packages.capability_mapping.infrastructure.adapters import (
    FileSystemCodebaseScannerAdapter,
    InMemoryCapabilityMappingRepository,
)


def test_capability_mapping_and_gap_analysis(tmp_path: Path) -> None:
    packages_dir = tmp_path / "packages"
    (packages_dir / "knowledge").mkdir(parents=True)
    (packages_dir / "identity").mkdir(parents=True)

    repo = InMemoryCapabilityMappingRepository()
    scanner = FileSystemCodebaseScannerAdapter()

    register_uc = RegisterCapabilityMappingUseCase(repo)
    analyze_uc = AnalyzeCapabilityGapsUseCase(repo, scanner)

    cmd = RegisterCapabilityMappingCommand(
        capability_id="CAP-KNW-01",
        capability_name="Knowledge Management",
        domain_group="Core",
        maturity_level=CapabilityMaturityLevel.OPTIMIZING,
        bindings=[
            BindingDTO(
                target_ref="packages/knowledge",
                realization_type=RealizationType.PACKAGE,
                description="Core knowledge domain package",
            ),
            BindingDTO(
                target_ref="packages/non_existing_billing",
                realization_type=RealizationType.PACKAGE,
                description="Missing billing package",
            ),
        ],
    )
    register_uc.execute(cmd)

    query = AnalyzeCapabilityGapsQuery(workspace_root=tmp_path)
    reports = analyze_uc.execute(query)

    assert len(reports) == 1
    report = reports[0]
    assert report.capability_id == "CAP-KNW-01"
    assert report.coverage_percentage == 50.0
    assert report.status == "DEGRADED"
    assert "packages/non_existing_billing" in report.broken_bindings


def test_capability_mapping_healthy_100_percent(tmp_path: Path) -> None:
    packages_dir = tmp_path / "packages"
    (packages_dir / "identity").mkdir(parents=True)

    repo = InMemoryCapabilityMappingRepository()
    scanner = FileSystemCodebaseScannerAdapter()

    register_uc = RegisterCapabilityMappingUseCase(repo)
    analyze_uc = AnalyzeCapabilityGapsUseCase(repo, scanner)

    cmd = RegisterCapabilityMappingCommand(
        capability_id="CAP-IDN-01",
        capability_name="Identity & Access",
        domain_group="Security",
        bindings=[
            BindingDTO(
                target_ref="packages/identity",
                realization_type=RealizationType.PACKAGE,
                description="Identity package",
            )
        ],
    )
    register_uc.execute(cmd)

    reports = analyze_uc.execute(
        AnalyzeCapabilityGapsQuery(workspace_root=tmp_path)
    )
    assert reports[0].coverage_percentage == 100.0
    assert reports[0].status == "HEALTHY"
    assert len(reports[0].broken_bindings) == 0
