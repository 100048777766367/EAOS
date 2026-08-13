"""Lightweight Temporal Hierarchy Index (Temporal View)."""

from __future__ import annotations

from typing import Final

from provenance.domain.models import TemporalIndexDTO


class TemporalIndex:
    """Index mapping temporal session turns to Raw Evidence IDs."""

    def __init__(self) -> None:
        self._indexes: Final[list[TemporalIndexDTO]] = []

    def index_turn(self, session_id: str, turn_id: int, evidence_id: str) -> TemporalIndexDTO:
        """Adds a light temporal hierarchy entry pointing to raw evidence."""
        entry = TemporalIndexDTO(
            session_id=session_id,
            turn_id=turn_id,
            evidence_id=evidence_id,
        )
        self._indexes.append(entry)
        return entry

    def find_evidence_ids(
        self,
        session_id: str | None = None,
        start_turn: int | None = None,
        end_turn: int | None = None,
    ) -> set[str]:
        """Finds raw evidence IDs matching strict temporal constraints."""
        matched: set[str] = set()
        for idx in self._indexes:
            if session_id and idx.session_id != session_id:
                continue
            if start_turn is not None and idx.turn_id < start_turn:
                continue
            if end_turn is not None and idx.turn_id > end_turn:
                continue
            matched.add(idx.evidence_id)
        return matched
