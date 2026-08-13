"""Deterministic Query Planner balancing Time vs Relation Priorities."""

from __future__ import annotations

from provenance.domain.models import QueryPlanDTO


class DeterministicQueryPlanner:
    """Parses query text to construct deterministic execution plans."""

    def plan_query(self, query_text: str, current_session_id: str | None = None) -> QueryPlanDTO:
        """Generates query plan using deterministic rule parsing."""
        lowered = query_text.lower()
        time_priority = 0.5
        relation_priority = 0.5

        if any(k in lowered for k in ("lúc nãy", "vừa rồi", "hôm qua", "turn", "session")):
            time_priority = 0.9
            relation_priority = 0.3

        if any(k in lowered for k in ("liên quan", "cấu trúc", "engine", "mô hình")):
            relation_priority = 0.9

        return QueryPlanDTO(
            time_priority=time_priority,
            relation_priority=relation_priority,
            session_id=current_session_id,
        )
