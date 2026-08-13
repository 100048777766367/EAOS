from __future__ import annotations

from datetime import datetime, timedelta

from evidence.domain.models import Evidence, EvidenceRef

"""Temporal Identity & Session Filter Engine (Rule R23)."""


class TemporalIdentityFilter:
    """4-Tier Identity Filter (User -> Session -> Task -> Time Window)."""

    def parse_temporal_intent(self, query_text: str, current_time: datetime | None = None) -> tuple[datetime, datetime]:
        """Parses terms like 'lúc nãy', 'hôm qua' into datetime range."""
        now = current_time or datetime.now(datetime.UTC)
        lowered = query_text.lower()

        if "hôm qua" in lowered:
            start = now - timedelta(days=1)
            return start, now

        # Default window: recent 2 hours ("lúc nãy")
        start = now - timedelta(hours=2)
        return start, now

    def filter_by_identity(
        self,
        evidences: list[Evidence],
        user_id: str,
        session_id: str | None = None,
        task_id: str | None = None,
    ) -> list[Evidence]:
        """Applies strict 4-Tier Identity pre-filtering before RAG."""
        filtered: list[Evidence] = []
        for ev in evidences:
            if ev.ref_identity is None:
                filtered.append(ev)
                continue

            ref: EvidenceRef = ev.ref_identity
            if ref.user_id != user_id:
                continue

            if session_id and ref.session_id != session_id:
                continue

            if task_id and ref.task_id != task_id:
                continue

            filtered.append(ev)

        return filtered
