"""Filesystem-backed verification evidence store."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class EvidenceStore:
    """Persist verification evidence under runtime evidence."""

    def __init__(self, project_root: Path) -> None:
        """Initialize evidence storage."""
        self.root = project_root.resolve() / "runtime" / "evidence" / "verification"
        self.root.mkdir(parents=True, exist_ok=True)

    def store(
        self,
        result: dict[str, Any],
    ) -> str:
        """Persist a verification result and return its evidence ID."""
        timestamp = datetime.now(UTC).strftime(
            "%Y%m%dT%H%M%S%fZ",
        )

        payload = json.dumps(
            result,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        )

        digest = hashlib.sha256(
            payload.encode("utf-8"),
        ).hexdigest()[:16]

        evidence_id = f"ver-{timestamp}-{digest}"

        path = self.root / f"{evidence_id}.json"

        document = {
            "evidence_id": evidence_id,
            "created_at": datetime.now(UTC).isoformat(),
            "result": result,
        }

        path.write_text(
            json.dumps(
                document,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return evidence_id
