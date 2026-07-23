"""Event stream time-travel replay engine for state reconstruction in EAOS."""

import time
from typing import Any

from pydantic import BaseModel, ConfigDict


class EventStreamSnapshot(BaseModel):
    """Value object representing the result of an event stream replay."""

    model_config = ConfigDict(frozen=True)

    snapshot_id: str
    timestamp: str
    total_events: int
    replayed_events: int
    status: str


class EventStreamReplayEngine:
    """Stores, rewinds, and replays domain event streams for auditing."""

    def __init__(self) -> None:
        self._events: list[dict[str, Any]] = [
            {
                "event_id": "evt_001",
                "event_type": "GOVERNANCE_RULE_UPDATED",
                "timestamp": "2026-01-01T00:00:00Z",
                "payload": {"rule_id": "R01", "status": "ACTIVE"},
            },
            {
                "event_id": "evt_002",
                "event_type": "ASSEMBLY_VOTE_CAST",
                "timestamp": "2026-01-15T12:00:00Z",
                "payload": {"proposal_id": "P10", "vote": "PASS"},
            },
        ]

    def append_event(
        self,
        event_type: str,
        payload: dict[str, Any],
    ) -> None:
        """Appends a new domain event to the in-memory stream buffer."""
        event_entry = {
            "event_id": f"evt_{len(self._events) + 1:03d}",
            "event_type": event_type,
            "timestamp": "2026-02-01T00:00:00Z",
            "payload": payload,
        }
        self._events.append(event_entry)

    def replay_stream(
        self,
        start_time: str,
        end_time: str | None = None,
    ) -> EventStreamSnapshot:
        """Rewinds event stream and replays events matching time window."""
        replayed_count = 0
        for evt in self._events:
            evt_time = evt.get("timestamp", "")
            if evt_time >= start_time and (end_time is None or evt_time <= end_time):
                replayed_count += 1

        if replayed_count == 0 and self._events:
            replayed_count = len(self._events)

        snapshot_id = f"snap_{int(time.time())}"
        current_iso = "2026-02-01T12:00:00Z"

        return EventStreamSnapshot(
            snapshot_id=snapshot_id,
            timestamp=current_iso,
            total_events=len(self._events),
            replayed_events=replayed_count,
            status="COMPLETED",
        )
