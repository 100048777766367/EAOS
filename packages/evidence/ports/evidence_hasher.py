from __future__ import annotations

from typing import Protocol

"""Hasher Port interface for Canonical Bound Evidence Hashing (Item 6 Fix)."""


class EvidenceHasherPort(Protocol):
    """Abstract port for bound canonical hash calculation."""

    def calculate_canonical_hash(
        self,
        evidence_id: str,
        evidence_type: str,
        user_id: str,
        session_id: str,
        turn_id: int,
        raw_content: str,
        metadata_str: str,
        previous_hash: str | None = None,
    ) -> tuple[str, str]:
        """Calculates (canonical_hash, chain_hash)."""
        ...
