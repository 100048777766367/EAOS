from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from dxs.evidence.hash import calculate_hash


class EvidenceLedger:
    def __init__(
        self,
        root: Path = Path("runtime/evidence/dxs"),
    ):
        self.root = root
        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def record(
        self,
        command: str,
        result: dict,
    ) -> Path:
        evidence = {
            "command": command,
            "timestamp": datetime.utcnow().isoformat(),
            "result": result,
        }

        evidence["hash"] = calculate_hash(evidence)

        filename = self.root / f"{command}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json"

        filename.write_text(
            json.dumps(
                evidence,
                indent=2,
                default=str,
            ),
            encoding="utf-8",
        )

        return filename
