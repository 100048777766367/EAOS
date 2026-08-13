from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from dxs.contracts.evidence import Evidence


def write_evidence(evidence: Evidence, root: Path) -> Path:
    target_dir = root / ".eaos" / "evidence" / "dxs" / "doctor"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "latest.json"
    target.write_text(
        json.dumps(asdict(evidence), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return target
