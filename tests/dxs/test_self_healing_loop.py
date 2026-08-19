from dxs.application.self_healing_orchestrator import SelfHealingOrchestrator
from dxs.governance.model import GovernanceDecision
from dxs.self_healing.engine import SelfHealingEngine


def test_self_healing_loop():
    engine = SelfHealingEngine()

    plan = engine.diagnose("dependency mismatch")

    result = engine.repair(plan)

    assert result.success

    assert engine.verify(result)


def test_application_self_healing_loop_records_evidence(tmp_path):
    orchestrator = SelfHealingOrchestrator(evidence_path=tmp_path)

    result = orchestrator.heal(
        "dependency mismatch",
        GovernanceDecision(
            allowed=True,
            rule="self_healing_allowed",
            reason="Policy permits deterministic repair.",
        ),
    )

    assert result.success
    assert result.evidence is not None
    assert result.evidence.exists()
