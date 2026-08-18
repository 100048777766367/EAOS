"""Runtime ledger proof helpers."""

from __future__ import annotations

import hashlib
import json
from typing import Any


class QuantumRuntimeLedger:
    """Generate stable hashes for runtime trace payloads."""

    @staticmethod
    def generate_trace_proof(
        trace_type: str,
        payload: dict[str, Any],
    ) -> str:
        """Return a deterministic SHA-256 proof for a trace payload."""
        body = {
            "payload": payload,
            "trace_type": trace_type,
        }
        canonical = json.dumps(
            body,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
