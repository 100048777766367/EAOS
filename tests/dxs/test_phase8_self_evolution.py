from dxs.discovery import CapabilityDiscoveryService
from dxs.evolutionary_evidence import (
    EvolutionaryEvidenceService,
)
from dxs.health import HealthService, HealthStatus
from dxs.migration import (
    MigrationReadiness,
    MigrationReadinessService,
)
from dxs.self_diagnostics import SelfDiagnosticsService


def test_self_diagnostics() -> None:
    finding = SelfDiagnosticsService().inspect_path(
        "dxs",
        True,
    )

    assert finding.passed is True


def test_capability_discovery_is_deterministic() -> None:
    result = CapabilityDiscoveryService().discover(
        (" z", "a", "z", " "),
        "test",
    )

    assert [item.name for item in result] == ["a", "z"]


def test_health_model() -> None:
    report = HealthService().evaluate(10, 0)

    assert report.status is HealthStatus.HEALTHY
    assert report.healthy is True


def test_migration_readiness() -> None:
    service = MigrationReadinessService()

    ready = service.evaluate(True, 0)
    blocked = service.evaluate(False, 1)

    assert ready.status is MigrationReadiness.READY
    assert blocked.status is MigrationReadiness.BLOCKED


def test_evolutionary_evidence() -> None:
    service = EvolutionaryEvidenceService()

    evidence = service.record(
        "gate",
        "all quality gates passed",
        "evolution permitted",
    )

    assert service.summarize((evidence,)) == ("gate: evolution permitted",)
