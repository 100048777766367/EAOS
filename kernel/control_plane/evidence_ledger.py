"""EAOS Evidence Ledger & Task Record Generator."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel, Field


class TaskEvidenceRecord(BaseModel):
    """Structured Evidence Record for an EAOS Engineering Task."""

    task_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    baseline_git_commit: str = "UNKNOWN"
    intent: str
    authority_level: str
    root_cause: str
    strategy: str
    blast_radius: str
    affected_files: list[str] = Field(default_factory=list)
    commands_executed: list[str] = Field(default_factory=list)
    verification_results: dict[str, str] = Field(default_factory=dict)
    decision: str = "UNKNOWN"
    rollback_checkpoint: str | None = None
    evidence_text: str = ""


class EvidenceLedger:
    """Evidence Ledger managing immutable task records."""

    def __init__(self, ledger_dir: Path | str = ".eaos_ledger") -> None:
        self.ledger_dir = Path(ledger_dir)
        self.ledger_dir.mkdir(parents=True, exist_ok=True)
        self._records: list[TaskEvidenceRecord] = []

    def record_task(self, record: TaskEvidenceRecord) -> Path:
        """Record task evidence and export to JSON & Markdown."""
        self._records.append(record)
        timestamp_slug = int(datetime.now(UTC).timestamp())
        file_name = f"task_{record.task_id}_{timestamp_slug}.json"
        target_path = self.ledger_dir / file_name
        target_path.write_text(json.dumps(record.model_dump(), indent=2), encoding="utf-8")
        return target_path

    def render_markdown(self, record: TaskEvidenceRecord) -> str:
        """Render a TaskEvidenceRecord into Markdown format."""
        files_md = chr(10).join(f"- `{f}`" for f in record.affected_files) if record.affected_files else "None"
        verif_md = (
            chr(10).join(f"- **{k}**: {v}" for k, v in record.verification_results.items())
            if record.verification_results
            else "None"
        )

        return f"""# EAOS Task Evidence Record — {record.task_id}

- **Timestamp**: `{record.timestamp}`
- **Baseline Git Commit**: `{record.baseline_git_commit}`
- **Authority Level**: `{record.authority_level}`
- **Strategy**: `{record.strategy}` (Blast Radius: `{record.blast_radius}`)
- **Final Decision**: `{record.decision}`

## Intent
{record.intent}

## Root Cause Analysis
{record.root_cause}

## Affected Files ({len(record.affected_files)})
{files_md}

## Verification Results
{verif_md}

## Evidence Summary
```text
{record.evidence_text}
"""
