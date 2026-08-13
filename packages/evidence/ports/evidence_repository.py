from __future__ import annotations

from typing import Protocol

from packages.evidence.domain.evidence import Evidence

"""Repository Port interface for Append-Only Evidence Storage (Item 6 Fix)."""


class EvidenceRepositoryPort(Protocol):
    """Abstract port for append-only evidence storage."""

    def append(self, evidence: Evidence) -> Evidence:
        """Appends evidence record."""
        ...

    def get_by_id(self, evidence_id: str) -> Evidence | None:
        """Retrieves evidence record by ID string."""
        ...

    def list_by_session(self, session_id: str) -> list[Evidence]:
        """Lists evidence records for a session."""
        ...
