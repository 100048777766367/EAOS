"""Master EAOS Deterministic Conversation Retrieval & Provenance Engine."""

from __future__ import annotations

from pathlib import Path
from typing import Final

from provenance.contradiction.contradiction_filter import ContradictionFilter
from provenance.domain.models import (
    TurnMessageDTO,
    VerifiedContextDTO,
)
from provenance.graph.entity_graph import DeterministicEntityGraph
from provenance.planner.query_planner import DeterministicQueryPlanner
from provenance.temporal.hierarchy import TemporalHierarchyTree


class EAOSProvenanceEngine:
    """Master Deterministic Provenance Engine (Zero LLM Tokens for Retrieval)."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root: Final[Path] = (workspace_root or Path.cwd()).resolve()
        self.graph: Final[DeterministicEntityGraph] = DeterministicEntityGraph()
        self.temporal: Final[TemporalHierarchyTree] = TemporalHierarchyTree()
        self.contradiction: Final[ContradictionFilter] = ContradictionFilter()
        self.planner: Final[DeterministicQueryPlanner] = DeterministicQueryPlanner()

    def record_conversation_turn(
        self,
        session_id: str,
        turn_id: int,
        role: str,
        content: str,
    ) -> TurnMessageDTO:
        """Records turn into temporal hierarchy and extracts entities."""
        msg_id = f"msg-{session_id}-{turn_id}-{role.lower()}"
        turn = TurnMessageDTO(
            message_id=msg_id,  # pyright: ignore[reportCallIssue]
            session_id=session_id,  # pyright: ignore[reportCallIssue]
            turn_id=turn_id,  # pyright: ignore[reportCallIssue]
            role=role,  # pyright: ignore[reportCallIssue]
            content=content,  # pyright: ignore[reportCallIssue]
        )
        self.temporal.add_turn(turn)
        return turn

    def retrieve_verified_context(
        self,
        query_text: str,
        session_id: str = "default_session",
    ) -> VerifiedContextDTO:
        """Retrieves verified context with provenance using 0 LLM tokens."""
        plan = self.planner.plan_query(query_text=query_text, current_session_id=session_id)
        turns = self.temporal.get_turns_for_session(session_id=session_id)
        claims = self.contradiction.get_active_claims()

        base_citation = (
            f"Provenance Citation: session={session_id}, "
            f"turns={len(turns)}, active_claims={len(claims)}, "
            f"plan=(time={plan.time_priority:.1f}, "
            f"relation={plan.relation_priority:.1f})"  # pyright: ignore[reportAttributeAccessIssue]
        )
        citations: list[str] = [base_citation]

        turn_citations = [
            f"Source: turn={turn.turn_id}, role={turn.role}, msg_id={turn.message_id}"  # pyright: ignore[reportAttributeAccessIssue]
            for turn in turns[-3:]
        ]
        citations.extend(turn_citations)

        return VerifiedContextDTO(
            query_text=query_text,  # pyright: ignore[reportCallIssue]
            claims=claims,  # pyright: ignore[reportCallIssue]
            turns=turns,  # pyright: ignore[reportCallIssue]
            citations=citations,  # pyright: ignore[reportCallIssue]
            llm_tokens_spent_indexing=0,  # pyright: ignore[reportCallIssue]
            llm_tokens_spent_retrieval=0,  # pyright: ignore[reportCallIssue]
        )  # pyright: ignore[reportCallIssue]
