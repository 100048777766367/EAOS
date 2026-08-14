from dxs.self_healing.engine import SelfHealingEngine


def test_self_healing_loop():
    engine = SelfHealingEngine()

    plan = engine.diagnose("dependency mismatch")

    result = engine.repair(plan)

    assert result.success

    assert engine.verify(result)
