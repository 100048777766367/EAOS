from pathlib import Path

from dxs.evolution.capability_discovery import CapabilityDiscovery
from dxs.evolution.health import (
    HealthCheck,
    HealthModel,
    HealthStatus,
)
from dxs.evolution.migration_readiness import (
    MigrationReadinessService,
)
from dxs.evolution.service import EvolutionService


def test_capability_discovery_uses_real_paths(tmp_path: Path) -> None:
    (tmp_path / "dxs").mkdir()
    (tmp_path / "tests" / "dxs").mkdir(parents=True)

    result = CapabilityDiscovery().discover(tmp_path)

    names = {item.name for item in result}

    assert "dxs" in names
    assert "tests" in names


def test_health_model_all_passed_is_healthy() -> None:
    checks = (
        HealthCheck(
            name="repository",
            passed=True,
            detail="ok",
        ),
    )

    result = HealthModel.from_checks(checks)

    assert result.status is HealthStatus.HEALTHY


def test_health_model_partial_is_degraded() -> None:
    checks = (
        HealthCheck(
            name="one",
            passed=True,
            detail="ok",
        ),
        HealthCheck(
            name="two",
            passed=False,
            detail="missing",
        ),
    )

    result = HealthModel.from_checks(checks)

    assert result.status is HealthStatus.DEGRADED


def test_migration_readiness_reports_blockers() -> None:
    result = MigrationReadinessService().evaluate(
        repository_healthy=False,
        contract_compatible=True,
        migration_requested=True,
    )

    assert result.ready is False
    assert "repository_health_not_healthy" in result.blockers


def test_migration_readiness_is_ready_when_safe() -> None:
    result = MigrationReadinessService().evaluate(
        repository_healthy=True,
        contract_compatible=True,
        migration_requested=False,
    )

    assert result.ready is True


def test_evolution_service_collects_real_evidence(
    tmp_path: Path,
) -> None:
    (tmp_path / "dxs").mkdir()

    service = EvolutionService()
    capabilities = service.discover(tmp_path)
    health = service.health(capabilities)

    readiness = service.migration_readiness(
        health=health,
        contract_compatible=True,
    )

    evidence = service.evidence(
        tmp_path,
        capabilities=capabilities,
        health=health,
        readiness=readiness,
    )

    assert evidence.repository_root == str(tmp_path)
    assert evidence.capability_count == len(capabilities)
    assert evidence.files_observed >= 0


def test_empty_health_is_degraded() -> None:
    result = HealthModel.from_checks(())

    assert result.status is HealthStatus.DEGRADED


def test_invalid_migration_input_is_not_silently_ready() -> None:
    result = MigrationReadinessService().evaluate(
        repository_healthy=True,
        contract_compatible=False,
        migration_requested=True,
    )

    assert result.ready is False


def test_discovery_result_is_deterministic(tmp_path: Path) -> None:
    (tmp_path / "dxs").mkdir()

    discovery = CapabilityDiscovery()

    first = discovery.discover(tmp_path)
    second = discovery.discover(tmp_path)

    assert first == second
