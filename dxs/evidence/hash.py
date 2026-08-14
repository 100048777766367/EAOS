"""Evidence integrity hashing utilities."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def calculate_hash(
    payload: dict[str, Any],
) -> str:
    """Create deterministic SHA256 evidence hash."""

    normalized = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    )

    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


class EvidenceHasher:
    """Object interface for evidence hashing."""

    def hash(
        self,
        payload: dict[str, Any],
    ) -> str:
        return calculate_hash(payload)


__all__ = [
    "EvidenceHasher",
    "calculate_hash",
]
