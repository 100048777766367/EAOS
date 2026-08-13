from __future__ import annotations

from typing import Final

from packages.provenance.domain.evidence import Evidence

"""Raw Evidence Store Adapter - Single Source of Truth."""


class RawEvidenceStore:
    """In-memory and file-backed raw evidence store."""

    def __init__(self) -> None:
        self._store: Final[dict[str, Evidence]] = {}

    def save(self, evidence: Evidence) -> Evidence:
        """Saves a raw evidence record."""
        self._store[evidence.evidence_id] = evidence
        return evidence

    def get_by_id(self, evidence_id: str) -> Evidence | None:
        """Retrieves raw evidence by ID."""
        return self._store.get(evidence_id)

    def list_all(self) -> list[Evidence]:
        """Lists all raw evidence records."""
        return list(self._store.values())
