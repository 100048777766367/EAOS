from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from dxs.bootstrap.composition import create_repository_application
from dxs.contracts.scaffolding import ScaffoldResult
from dxs.contracts.versioning import ContractVersion
from dxs.domain.compatibility import CompatibilityResult
from dxs.domain.repository import RepositoryContext
from dxs.domain.validation import ValidationResult
from dxs.evidence.model import Evidence, EvidenceStatus
from dxs.health.model import HealthReport, HealthStatus
from dxs.remediation.model import Remediation, RemediationStatus


def test_repository_application_composition_root() -> None:
    application = create_repository_application()

    assert application is not None

    for method in (
        "discover",
        "inspect",
        "validate",
        "compatibility",
        "health",
        "evidence",
        "remediation",
        "scaffold",
    ):
        assert callable(getattr(application, method, None))


def test_health_contract_returns_health_report() -> None:
    application = create_repository_application()

    result = application.health(
        passed=10,
        failed=0,
    )

    assert isinstance(result, HealthReport)
    assert result.status is HealthStatus.HEALTHY
    assert result.passed == 10
    assert result.failed == 0
    assert result.healthy is True


def test_health_contract_degraded_state() -> None:
    application = create_repository_application()

    result = application.health(
        passed=9,
        failed=1,
    )

    assert isinstance(result, HealthReport)
    assert result.status is HealthStatus.DEGRADED
    assert result.passed == 9
    assert result.failed == 1
    assert result.healthy is False


def test_evidence_contract_returns_open_evidence() -> None:
    application = create_repository_application()

    result = application.evidence(
        key="phaseC.contract",
        value="verified",
        source="phaseC_integration_test",
    )

    assert isinstance(result, Evidence)
    assert result.key == "phaseC.contract"
    assert result.value == "verified"
    assert result.source == "phaseC_integration_test"
    assert result.status is EvidenceStatus.OPEN


def test_remediation_contract_returns_open_remediation() -> None:
    application = create_repository_application()

    result = application.remediation(
        key="phaseC.none",
        description="No remediation required.",
    )

    assert isinstance(result, Remediation)
    assert result.key == "phaseC.none"
    assert result.description == "No remediation required."
    assert result.status is RemediationStatus.OPEN


def test_discover_contract_returns_repository_context() -> None:
    application = create_repository_application()

    with TemporaryDirectory() as directory:
        root = Path(directory)

        result = application.discover(root)

        assert isinstance(result, RepositoryContext)


def test_inspect_contract_returns_findings() -> None:
    application = create_repository_application()

    with TemporaryDirectory() as directory:
        root = Path(directory)

        result = application.inspect(root)

        assert isinstance(result, list)
        assert all(isinstance(item, str) for item in result)


def test_validate_contract_returns_validation_results() -> None:
    application = create_repository_application()

    with TemporaryDirectory() as directory:
        root = Path(directory)

        result = application.validate(root)

        assert isinstance(result, list)
        assert all(isinstance(item, ValidationResult) for item in result)


def test_compatibility_contract_returns_result() -> None:
    application = create_repository_application()

    current = ContractVersion(major=1, minor=0, patch=0)
    target = ContractVersion(major=1, minor=0, patch=0)

    result = application.compatibility(
        current=current,
        target=target,
    )

    assert isinstance(result, CompatibilityResult)
    assert result.compatible is True


def test_scaffold_contract_returns_scaffold_result() -> None:
    application = create_repository_application()

    with TemporaryDirectory() as directory:
        root = Path(directory)

        result = application.scaffold(
            root=root,
            name="phaseC_capability",
        )

        assert isinstance(result, ScaffoldResult)

        expected = (
            "domain/__init__.py",
            "application/__init__.py",
            "ports/__init__.py",
            "adapters/__init__.py",
            "tests/__init__.py",
            "README.md",
        )

        target = root / "phaseC_capability"

        assert target.exists()
        assert target.is_dir()

        for relative in expected:
            assert (target / relative).exists()

        assert len(result.created) == 6
        assert len(result.skipped) == 0


def test_scaffold_contract_is_idempotent() -> None:
    application = create_repository_application()

    with TemporaryDirectory() as directory:
        root = Path(directory)

        first = application.scaffold(
            root=root,
            name="phaseC_idempotent",
        )

        second = application.scaffold(
            root=root,
            name="phaseC_idempotent",
        )

        assert isinstance(first, ScaffoldResult)
        assert isinstance(second, ScaffoldResult)

        assert len(first.created) == 6
        assert len(second.created) == 0
        assert len(second.skipped) == 6

