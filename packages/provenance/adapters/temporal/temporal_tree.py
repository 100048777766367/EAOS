from __future__ import annotations

from typing import Final

from packages.provenance.domain.temporal import TemporalHierarchy

"""Temporal Tree Adapter mapping Session and Turn hierarchies to evidence IDs."""


class TemporalTreeAdapter:
    """Temporal hierarchy tree index adapter."""

    def __init__(self) -> None:
        self._hierarchy: Final[list[TemporalHierarchy]] = []

    def index_turn(
        self,
        user_id: str,
        session_id: str,
        turn_id: int,
        evidence_id: str,
        conversation_id: str = "conv-001",
    ) -> TemporalHierarchy:
        """Indexes a temporal hierarchy turn entry."""
        entry = TemporalHierarchy(
            user_id=user_id,
            conversation_id=conversation_id,
            session_id=session_id,
            turn_id=turn_id,
            evidence_id=evidence_id,
        )
        self._hierarchy.append(entry)
        return entry

    def find_evidence_ids_by_temporal_range(
        self,
        user_id: str,
        session_id: str | None = None,
        start_turn: int | None = None,
        end_turn: int | None = None,
    ) -> set[str]:
        """Finds evidence IDs matching strict user, session, and turn constraints."""
        matched: set[str] = set()
        for node in self._hierarchy:
            if node.user_id != user_id:
                continue
            if session_id and node.session_id != session_id:
                continue
            if start_turn is not None and node.turn_id < start_turn:
                continue
            if end_turn is not None and node.turn_id > end_turn:
                continue
            matched.add(node.evidence_id)
        return matched
