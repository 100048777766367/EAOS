from __future__ import annotations

from pathlib import Path
from typing import Final

from evidence.domain.models import Evidence, EvidenceBundleDTO
from evidence.identity.temporal_filter import TemporalIdentityFilter
from evidence.retrieval.hybrid_retriever import HybridEvidenceRetriever
from evidence.verification.evidence_verifier import EvidenceVerifier

"""Master EAOS Enterprise Evidence Engine Orchestrator."""


class EAOSEnterpriseEvidenceEngine:
    """Master Orchestrator for Grounded Temporal Evidence Retrieval."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root: Final[Path] = (workspace_root or Path.cwd()).resolve()
        self.filter: Final[TemporalIdentityFilter] = TemporalIdentityFilter()
        self.retriever: Final[HybridEvidenceRetriever] = HybridEvidenceRetriever()
        self.verifier: Final[EvidenceVerifier] = EvidenceVerifier(self.root)

    def assemble_grounded_bundle(
        self,
        query_text: str,
        user_id: str,
        session_id: str = "session-001",
        top_k: int = 3,
    ) -> EvidenceBundleDTO:
        """Assembles verified, temporal-identity filtered Evidence Bundle."""
        raw_candidates = self.retriever.search(query=query_text, top_k=top_k)
        identity_filtered = self.filter.filter_by_identity(
            evidences=raw_candidates,
            user_id=user_id,
            session_id=session_id,
        )

        verified_list: list[Evidence] = []
        for ev in identity_filtered:
            checked = self.verifier.verify_evidence(ev)
            if checked.is_verified and checked.relevance_score > 0.0:
                verified_list.append(checked)

        return EvidenceBundleDTO(
            bundle_id=f"bundle-{user_id.lower()}-{session_id.lower()}",
            query_text=query_text,
            user_identity=user_id,
            session_identity=session_id,
            trusted_evidences=verified_list,
            total_evidences_verified=len(verified_list),
            confidence_score=1.0 if verified_list else 0.5,
        )
