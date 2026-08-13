"""Execution evidence store."""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class ExecutionEvidenceStore:
    """Persist execution evidence into EAOS evidence storage."""

    def __init__(self, project_root: Path) -> None:
        self.root = project_root.resolve()
        self.directory = self.root / ".eaos" / "evidence"
        self.directory.mkdir(parents=True, exist_ok=True)

        self.path = self.directory / "agent-execution.jsonl"

    def store(self, payload: dict[str, Any]) -> str:
        """Persist evidence and return evidence ID."""
        evidence_id = "agent-" + datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ") + "-" + uuid.uuid4().hex[:12]

        record = {
            "evidence_id": evidence_id,
            "created_at": datetime.now(UTC).isoformat(),
            "payload": payload,
        }

        with self.path.open(
            "a",
            encoding="utf-8",
            newline="\n",
        ) as handle:
            handle.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )

        return evidence_id
