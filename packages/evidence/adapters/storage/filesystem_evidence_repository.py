from __future__ import annotations

import threading
from pathlib import Path
from typing import Final

from packages.evidence.domain.evidence import Evidence

"""Thread-Safe Append-Only Filesystem Repository Adapter (Items 1, 5, 12, 14 Fix)."""


class DuplicateEvidenceIdError(Exception):
    """Raised when attempting to append duplicate evidence ID."""


class OutOfOrderSequenceError(Exception):
    """Raised when turn sequence is out of order."""


class FilesystemEvidenceRepositoryAdapter:
    """Thread-safe persistent append-only filesystem evidence repository."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root: Final[Path] = (workspace_root or Path.cwd()).resolve()
        self.store_dir: Final[Path] = self.root / ".memory" / "evidence_store"
        self.store_dir.mkdir(parents=True, exist_ok=True)
        self._index: Final[dict[str, Evidence]] = {}
        self._lock: Final[threading.RLock] = threading.RLock()

    def append(self, evidence: Evidence) -> Evidence:
        """Appends a new evidence record with thread lock & append-only check."""
        with self._lock:
            ev_str_id = evidence.evidence_id.value
            if ev_str_id in self._index:
                raise DuplicateEvidenceIdError(
                    f"Append-only Invariant Breach: Evidence ID '{ev_str_id}' already exists."
                )

            session_evs = self.list_by_session(evidence.session_id)
            if session_evs:
                last_turn = session_evs[-1].turn_id
                if evidence.turn_id < last_turn:
                    raise OutOfOrderSequenceError(
                        f"Out-of-Order Sequence Error: Turn {evidence.turn_id} "
                        f"is lower than last session turn {last_turn}."
                    )

            self._index[ev_str_id] = evidence
            file_path = self.store_dir / f"{ev_str_id}.json"
            file_path.write_text(evidence.model_dump_json(indent=2), encoding="utf-8")
            return evidence

    def get_by_id(self, evidence_id: str) -> Evidence | None:
        """Retrieves evidence record by string ID with thread lock."""
        with self._lock:
            return self._index.get(evidence_id)

    def list_by_session(self, session_id: str) -> list[Evidence]:
        """Lists evidence records for a session ordered by turn_id."""
        with self._lock:
            records = [ev for ev in self._index.values() if ev.session_id == session_id]
            records.sort(key=lambda x: x.turn_id)
            return records
