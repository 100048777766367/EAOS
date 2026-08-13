from __future__ import annotations

from packages.evidence.domain.evidence import Evidence
from packages.evidence.domain.evidence_bundle import EvidenceBundleDTO
from packages.evidence.integrity.chain_verifier import ChainVerifier

"""Evidence Bundle Builder with Filtered ID Selection (Item 8 Fix)."""


class EvidenceBundleBuilder:
    """Assembles bundle filtering specific requested IDs without dumping entire session."""

    def __init__(self) -> None:
        self.chain_verifier = ChainVerifier()

    def build_bundle_by_ids(
        self,
        bundle_id: str,
        query_text: str,
        target_evidence_ids: list[str],
        session_evidences: list[Evidence],
    ) -> EvidenceBundleDTO:
        """Filters requested IDs and verifies cryptographic chain integrity."""
        id_set = set(target_evidence_ids)
        filtered_evs = [ev for ev in session_evidences if ev.evidence_id.value in id_set]

        valid, events = self.chain_verifier.verify_chain(session_evidences)
        return EvidenceBundleDTO(
            bundle_id=bundle_id,
            query_text=query_text,
            evidences=filtered_evs,
            total_count=len(filtered_evs),
            chain_valid=valid,
            tamper_detected=len(events) > 0,
        )
