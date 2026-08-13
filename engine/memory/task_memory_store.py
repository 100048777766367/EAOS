"""Task Memory Store persisting lifecycle execution history and evidence tokens."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class EngineeringTaskRecordDTO:
    """Canonical persistent record of a completed or escalated engineering task."""

    loop_id: str
    task_id: str
    intent_summary: str
    system_state: str
    strategy: str
    authority: str
    blast_radius: str
    is_converged: bool
    evidence_token: str
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class TaskMemoryStore:
    """Stores and retrieves historical engineering task execution records."""

    def __init__(self) -> None:
        self._records: dict[str, EngineeringTaskRecordDTO] = {}

    def save_record(self, record: EngineeringTaskRecordDTO) -> None:
        """Saves an engineering task record."""
        self._records[record.loop_id] = record

    def get_record(self, loop_id: str) -> EngineeringTaskRecordDTO | None:
        """Retrieves an engineering task record by loop ID."""
        return self._records.get(loop_id)

    def list_all_records(self) -> list[EngineeringTaskRecordDTO]:
        """Lists all stored engineering task records."""
        return list(self._records.values())
