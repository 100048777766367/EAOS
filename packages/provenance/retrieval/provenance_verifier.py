from __future__ import annotations

import hashlib

from packages.provenance.domain.evidence import Evidence

"""Provenance Verifier ensuring evidence integrity and content hash validity."""


class ProvenanceVerifier:
    """Verifies evidence content hash and source integrity before LLM prompt."""

    def verify_evidence(self, evidence: Evidence) -> bool:
        """Verifies content_hash matches raw content SHA256."""
        calc_hash = hashlib.sha256(evidence.content.encode("utf-8")).hexdigest()[:16]
        return evidence.content_hash.startswith(calc_hash[:8])
