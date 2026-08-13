from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Final

"""Action Journal for Audit Provenance Tracking."""


@dataclass(frozen=True)
class JournalEntryDTO:
    """Immutable audit entry recording a turn event."""

    entry_id: str
    session_id: str
    turn_id: int
    actor: str
    action_name: str
    status: str
    timestamp: datetime = field(default_factory=datetime.utcnow)


class ActionJournal:
    """Audit log tracking every turn event from proposal to commit."""

    def __init__(self) -> None:
        self._entries: Final[list[JournalEntryDTO]] = []

    def log_event(
        self,
        session_id: str,
        turn_id: int,
        actor: str,
        action_name: str,
        status: str,
    ) -> JournalEntryDTO:
        """Appends an immutable event entry to the journal."""
        entry = JournalEntryDTO(
            entry_id=f"jnl-{len(self._entries) + 1}",
            session_id=session_id,
            turn_id=turn_id,
            actor=actor,
            action_name=action_name,
            status=status,
        )
        self._entries.append(entry)
        return entry

    def list_entries(self) -> list[JournalEntryDTO]:
        """Returns all audit journal entries."""
        return list(self._entries)
