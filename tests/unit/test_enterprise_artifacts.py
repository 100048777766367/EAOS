"""Unit test suite verifying integrity of Enterprise Artifacts."""

from pathlib import Path

from packages.governance.application.use_cases import (
    EvaluateGovernanceUseCase,
)
from packages.governance.domain.models import (
    ArchitecturalMaturityLevel,
    ConstitutionalRule,
    ConstitutionAmendment,
)


def test_governance_use_case_execution() -> None:
    """Verifies constitutional governance evaluation logic."""
    rule = ConstitutionalRule(
        rule_id="R01",
        title="Hexagonal Boundary",
        statement="Domain layer must remain clean",
    )
    amendment = ConstitutionAmendment(
        amendment_id="AMD-01",
        target_rule="R01",
        proposed_text="Strict typing mandated across domain",
        reasoning="Type safety enforcement",
    )
    uc = EvaluateGovernanceUseCase()
    assert uc.execute(rule, amendment) is True


def test_architectural_maturity_levels() -> None:
    """Verifies 5-tier Architectural Maturity Level enumeration."""
    assert ArchitecturalMaturityLevel.LEVEL_1_STATIC.value == "STATIC"
    assert ArchitecturalMaturityLevel.LEVEL_2_EXECUTABLE.value == "EXECUTABLE"
    assert ArchitecturalMaturityLevel.LEVEL_3_OBSERVABLE.value == "OBSERVABLE"
    assert ArchitecturalMaturityLevel.LEVEL_4_ADAPTIVE.value == "ADAPTIVE"
    assert ArchitecturalMaturityLevel.LEVEL_5_EVOLUTIONARY.value == "EVOLUTIONARY"


def test_enterprise_artifact_files_exist() -> None:
    """Verifies physical presence of declarative EA artifacts."""
    root = Path(".")
    assert (root / "infra" / "postgres" / "migrations" / "V001__init_eaos_schema.sql").exists()
    assert (root / "policies" / "security" / "rbac.rego").exists()
    assert (root / "contracts" / "proto" / "governance_v1.proto").exists()
