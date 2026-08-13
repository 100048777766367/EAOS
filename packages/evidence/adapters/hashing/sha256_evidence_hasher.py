from __future__ import annotations

import hashlib

"""Bound SHA-256 Canonical Hasher Adapter (Items 2 & 3 Fix)."""


class SHA256EvidenceHasherAdapter:
    """Calculates canonical hashes binding id, type, user, session, turn, content & metadata."""

    def calculate_canonical_hash(
        self,
        evidence_id: str,
        evidence_type: str,
        user_id: str,
        session_id: str,
        turn_id: int,
        raw_content: str,
        metadata_str: str = "",
        previous_hash: str | None = None,
    ) -> tuple[str, str]:
        """Returns bound (canonical_hash, chain_hash)."""
        canonical_payload = (
            f"id={evidence_id}|type={evidence_type}|user={user_id}|"
            f"session={session_id}|turn={turn_id}|content={raw_content}|"
            f"meta={metadata_str}"
        )
        canon_hash = hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()

        prev_str = previous_hash or "GENESIS_PREVIOUS_HASH"
        chain_payload = f"prev={prev_str}|canon={canon_hash}"
        chain_hash = hashlib.sha256(chain_payload.encode("utf-8")).hexdigest()

        return canon_hash, chain_hash
