"""Autonomous bug auto-fix recorder and evidence logger for EAOS."""

import json
import time
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict


class ErrorRecordDTO(BaseModel):
    """Value object representing an auto-fixed error log record."""

    model_config = ConfigDict(frozen=True)

    error_id: str
    command: str
    os_platform: str
    error_message: str
    root_cause: str
    remediation_patch: str
    status: str
    timestamp: str


class AutoFixHistoryEngine:
    """Engine recording bug fixes into organizational memory and ledgers."""

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()
        self.evidence_file: Path = self.root_dir / "knowledge" / "evidence" / "error_history.json"
        self.doc_file: Path = self.root_dir / "docs" / "operations" / "ERROR_HISTORY.md"

    def log_fix(
        self,
        command: str,
        os_platform: str,
        error_message: str,
        root_cause: str,
        remediation: str,
    ) -> ErrorRecordDTO:
        """Logs auto-fixed error to JSON evidence and Markdown history."""
        record = ErrorRecordDTO(
            error_id=f"ERR-{int(time.time())}",
            command=command,
            os_platform=os_platform,
            error_message=error_message,
            root_cause=root_cause,
            remediation_patch=remediation,
            status="AUTO_FIXED",
            timestamp="2026-07-23T20:10:00Z",
        )

        self._append_json_evidence(record)
        self._append_markdown_doc(record)
        return record

    def _append_json_evidence(self, record: ErrorRecordDTO) -> None:
        """Appends error record to knowledge/evidence/error_history.json."""
        self.evidence_file.parent.mkdir(parents=True, exist_ok=True)
        existing: list[dict[str, Any]] = []

        if self.evidence_file.exists():
            try:
                data = json.loads(self.evidence_file.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    existing = data
            except Exception:
                pass

        existing.append(record.model_dump())
        self.evidence_file.write_text(
            json.dumps(existing, indent=2),
            encoding="utf-8",
        )

    def _append_markdown_doc(self, record: ErrorRecordDTO) -> None:
        """Appends markdown summary to docs/operations/ERROR_HISTORY.md."""
        self.doc_file.parent.mkdir(parents=True, exist_ok=True)
        header = (
            "# EAOS Autonomous Bug Fix History & Learning Log\n\n"
            "| Error ID | Platform | Command | Root Cause | Status |\n"
            "| :--- | :--- | :--- | :--- | :--- |\n"
        )

        if not self.doc_file.exists():
            self.doc_file.write_text(header, encoding="utf-8")

        row = (
            f"| {record.error_id} | {record.os_platform} | "
            f"{record.command} | {record.root_cause} | "
            f"**{record.status}** |\n"
        )
        with self.doc_file.open("a", encoding="utf-8") as f:
            f.write(row)
