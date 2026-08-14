"""Evidence governance timeline."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class TimelineEvent:
    """
    Evidence timeline event.
    """

    hash: str
    action: str
    timestamp: str
    metadata: dict


class EvidenceTimeline:
    """
    Timeline reader for evidence ledger.
    """

    def __init__(
        self,
        root: Path,
    ) -> None:
        self._root = Path(root)

    def list_events(self) -> list[dict]:
        """
        Load evidence events from ledger.
        """

        events: list[dict] = []

        if not self._root.exists():
            return events

        for file in sorted(self._root.glob("*.json")):
            try:
                payload = json.loads(file.read_text(encoding="utf-8"))

                events.append(
                    {
                        "hash": payload.get("hash"),
                        "action": payload.get("action"),
                        "timestamp": payload.get("timestamp"),
                        **payload,
                    }
                )

            except json.JSONDecodeError:
                continue

        return events

    def append(
        self,
        event: TimelineEvent,
    ) -> None:
        """
        Append timeline event.
        """

        self._root.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = f"{event.timestamp.replace(':', '-')}.json"

        path = self._root / filename

        path.write_text(
            json.dumps(
                {
                    "hash": event.hash,
                    "action": event.action,
                    "timestamp": event.timestamp,
                    "metadata": event.metadata,
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    def snapshot(self) -> dict:
        """
        Governance snapshot.
        """

        return {
            "count": len(self.list_events()),
            "generated_at": datetime.now(UTC).isoformat(),
            "events": self.list_events(),
        }
