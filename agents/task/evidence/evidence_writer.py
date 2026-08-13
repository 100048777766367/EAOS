"""Evidence writer for Agent Tasks."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from agents.task.models.task_models import (
    AgentTask,
    TaskResult,
)


class EvidenceWriter:
    """Persist task evidence under the EAOS evidence directory."""

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root.resolve()

    def write(
        self,
        task: AgentTask,
        result: TaskResult,
    ) -> str:
        """Write one JSON evidence record."""

        evidence_id = f"evd-{datetime.now(UTC):%Y%m%dT%H%M%S}-{uuid4().hex[:8]}"

        evidence_dir = self.project_root / ".eaos" / "evidence"
        evidence_dir.mkdir(parents=True, exist_ok=True)

        path = evidence_dir / f"{evidence_id}.json"

        payload = {
            "evidence_id": evidence_id,
            "task_id": task.task_id,
            "request_id": task.request_id,
            "state": result.state.value,
            "success": result.success,
            "message": result.message,
            "patch_id": result.patch_id,
            "created_at": datetime.now(UTC).isoformat(),
        }

        path.write_text(
            json.dumps(
                payload,
                indent=2,
            ),
            encoding="utf-8",
        )

        return evidence_id
