from pathlib import Path

from dxs.application.self_healing_orchestrator import SelfHealingOrchestrator
from dxs.governance.model import GovernanceDecision
from dxs.self_healing.engine import SelfHealingEngine
from dxs.self_healing.model import HealingAction, HealingStatus


def test_engine_preserves_domain_execution_semantics():
    engine = SelfHealingEngine()

    result = engine.execute(
        HealingAction.REPAIR,
        {"component": "diagnostics"},
    )

    assert result.status == HealingStatus.HEALED
    assert result.evidence is None
    assert engine.verify(result)


def test_orchestrator_allow_records_healed_evidence(tmp_path: Path):
    orchestrator = SelfHealingOrchestrator(evidence_path=tmp_path)

    result = orchestrator.execute(
        HealingAction.REPAIR,
        {
            "component": "diagnostics",
            "detection": "failed_check",
        },
        GovernanceDecision(
            allowed=True,
            rule="self_healing_allowed",
            reason="Policy permits deterministic repair.",
        ),
        rollback_supported=True,
    )

    assert result.status == HealingStatus.HEALED
    assert result.rollback_supported
    assert result.evidence is not None
    assert result.evidence.exists()
    assert result.hash


def test_orchestrator_deny_records_blocked_evidence(tmp_path: Path):
    orchestrator = SelfHealingOrchestrator(evidence_path=tmp_path)

    result = orchestrator.execute(
        HealingAction.REPAIR,
        {"component": "diagnostics"},
        GovernanceDecision(
            allowed=False,
            rule="manual_approval_required",
            reason="Human approval is required.",
        ),
    )

    assert not result.success
    assert result.status == HealingStatus.BLOCKED
    assert result.evidence is not None
    assert result.evidence.exists()


def test_orchestrator_records_failed_execution_evidence(tmp_path: Path):
    orchestrator = SelfHealingOrchestrator(evidence_path=tmp_path)

    result = orchestrator.execute(
        HealingAction.REPAIR,
        {"component": "diagnostics", "force_failure": True},
        GovernanceDecision(
            allowed=True,
            rule="self_healing_allowed",
            reason="Policy permits deterministic repair.",
        ),
    )

    assert not result.success
    assert result.status == HealingStatus.FAILED
    assert result.evidence is not None
    assert result.evidence.exists()


def test_orchestrator_records_validation_failure_evidence(tmp_path: Path):
    orchestrator = SelfHealingOrchestrator(evidence_path=tmp_path)

    result = orchestrator.execute(
        HealingAction.REPAIR,
        {"component": "diagnostics"},
        GovernanceDecision(
            allowed=True,
            rule="self_healing_allowed",
            reason="Policy permits deterministic repair.",
        ),
        validation=lambda _: False,
    )

    assert not result.success
    assert result.status == HealingStatus.FAILED
    assert result.message == "Healing validation failed"
    assert result.evidence is not None
    assert result.evidence.exists()
