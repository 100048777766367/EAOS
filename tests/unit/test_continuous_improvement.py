"""Unit tests for Continuous Improvement (Kaizen) context."""

from packages.continuous_improvement.application.dto import (
    IdentifyOpportunitiesCommand,
    VerifyInitiativeCommand,
)
from packages.continuous_improvement.application.use_cases import (
    IdentifyImprovementOpportunitiesUseCase,
    VerifyInitiativeEffectivenessUseCase,
)
from packages.continuous_improvement.domain.models import (
    ImprovementCategory,
    InitiativeStatus,
)
from packages.continuous_improvement.infrastructure.adapters import (
    InMemoryImprovementRepository,
)


def test_identify_and_verify_kaizen_initiative_success() -> None:
    repo = InMemoryImprovementRepository()
    identify_uc = IdentifyImprovementOpportunitiesUseCase(repo)
    verify_uc = VerifyInitiativeEffectivenessUseCase(repo)

    # 1. Component with High Drift Index (0.25 > 0.15) triggers Decouple initiative
    cmd = IdentifyOpportunitiesCommand(
        target_component="packages/knowledge",
        health_score=85.0,
        drift_index=0.25,
        latency_ms=150.0,
    )

    dto = identify_uc.execute(cmd)

    assert dto is not None
    assert dto.category == ImprovementCategory.DECOUPLE_BOUNDARIES
    assert dto.baseline_value == 0.25
    assert dto.target_value == 0.05
    assert dto.roi_score > 0.0

    # 2. Verify Post-Execution: Drift reduced to 0.04 (Better than baseline 0.25)
    success = verify_uc.execute(
        VerifyInitiativeCommand(
            initiative_id=dto.initiative_id,
            current_metric_value=0.04,
        )
    )

    assert success is True
    updated_initiative = repo.find_by_id(dto.initiative_id)
    assert updated_initiative is not None
    assert updated_initiative.status == InitiativeStatus.VERIFIED


def test_verify_kaizen_initiative_failure_triggers_rollback() -> None:
    repo = InMemoryImprovementRepository()
    identify_uc = IdentifyImprovementOpportunitiesUseCase(repo)
    verify_uc = VerifyInitiativeEffectivenessUseCase(repo)

    # 1. Low Health Score (70.0 < 80.0) triggers Refactor initiative
    cmd = IdentifyOpportunitiesCommand(
        target_component="packages/identity",
        health_score=70.0,
        drift_index=0.02,
        latency_ms=100.0,
    )

    dto = identify_uc.execute(cmd)
    assert dto is not None
    assert dto.category == ImprovementCategory.REFACTOR_CODE

    # 2. Verify Post-Execution: Health Score dropped further to 65.0 (Worse!)
    success = verify_uc.execute(
        VerifyInitiativeCommand(
            initiative_id=dto.initiative_id,
            current_metric_value=65.0,
        )
    )

    assert success is False
    updated_initiative = repo.find_by_id(dto.initiative_id)
    assert updated_initiative is not None
    assert updated_initiative.status == InitiativeStatus.ROLLED_BACK
