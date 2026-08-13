"""Temporal Hierarchy Tree Engine (Year -> Month -> Day -> Session -> Turn)."""

from __future__ import annotations

from typing import Final

from provenance.domain.models import TurnMessageDTO


class TemporalHierarchyTree:
    """Manages session turns and strict temporal order traversal."""

    def __init__(self) -> None:
        self._turns_by_session: Final[dict[str, list[TurnMessageDTO]]] = {}

    def add_turn(self, turn: TurnMessageDTO) -> None:
        """Appends a turn message to its temporal session hierarchy."""
        if turn.session_id not in self._turns_by_session:
            self._turns_by_session[turn.session_id] = []
        self._turns_by_session[turn.session_id].append(turn)
        self._turns_by_session[turn.session_id].sort(key=lambda t: t.turn_id)

    def get_turns_for_session(
        self,
        session_id: str,
        start_turn: int | None = None,
        end_turn: int | None = None,
    ) -> list[TurnMessageDTO]:
        """Retrieves turns for a specific session within turn range."""
        turns = self._turns_by_session.get(session_id, [])
        if start_turn is not None:
            turns = [t for t in turns if t.turn_id >= start_turn]
        if end_turn is not None:
            turns = [t for t in turns if t.turn_id <= end_turn]
        return turns
