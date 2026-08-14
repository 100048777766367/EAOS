from pathlib import Path

from dxs.self_healing.engine import SelfHealingEngine
from dxs.self_healing.model import HealingAction


def test_evidence_backed_healing(tmp_path: Path):

    engine = SelfHealingEngine(tmp_path)

    result = engine.execute(
        HealingAction.REPAIR,
        {
            "component": "diagnostics",
            "reason": "failed_check",
        },
    )

    assert result.status == "HEALED"
    assert result.evidence.exists()
    assert result.hash
