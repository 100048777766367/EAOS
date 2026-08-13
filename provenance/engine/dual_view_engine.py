"""Deterministic Dual-Projection View Query Engine (FILTER -> INTERSECT -> VERIFY)."""

from __future__ import annotations

from typing import Final

from provenance.domain.models import (
    ConstraintFilterDTO,
    RawEvidenceNodeDTO,
    VerifiedEvidenceBundleDTO,
)
from provenance.indexes.relation_index import RelationIndex
from provenance.indexes.temporal_index import TemporalIndex


class DualViewQueryEngine:
    """Executes deterministic FILTER -> INTERSECT -> VERIFY pipeline."""

    def __init__(self, relation_idx: RelationIndex, temporal_idx: TemporalIndex) -> None:
        self.relation_idx: Final[RelationIndex] = relation_idx
        self.temporal_idx: Final[TemporalIndex] = temporal_idx
        self._raw_store: Final[dict[str, RawEvidenceNodeDTO]] = {}

    def store_raw_evidence(self, evidence: RawEvidenceNodeDTO) -> RawEvidenceNodeDTO:
        """Stores raw evidence as single source of truth."""
        self._raw_store[evidence.evidence_id] = evidence
        self.temporal_idx.index_turn(
            session_id=evidence.session_id,
            turn_id=evidence.turn_id,
            evidence_id=evidence.evidence_id,
        )
        return evidence

    def query_dual_views(
        self,
        query_text: str,
        constraints: ConstraintFilterDTO,
    ) -> VerifiedEvidenceBundleDTO:
        """Performs FILTER -> INTERSECT -> VERIFY to retrieve exact raw evidence."""
        # 1. Temporal View Candidate Set
        temporal_candidates = self.temporal_idx.find_evidence_ids(
            session_id=constraints.target_session_id,
            start_turn=constraints.start_turn,
            end_turn=constraints.end_turn,
        )

        # 2. Relation View Candidate Set
        relation_candidates: set[str] = set()
        if constraints.target_entity:
            relation_candidates = self.relation_idx.find_evidence_ids(entity_name=constraints.target_entity)

        # 3. INTERSECT Dual Views (Temporal Candidates ∩ Relation Candidates)
        if relation_candidates and temporal_candidates:
            intersected_ids = temporal_candidates.intersection(relation_candidates)
            if not intersected_ids:
                intersected_ids = temporal_candidates
        elif temporal_candidates:
            intersected_ids = temporal_candidates
        elif relation_candidates:
            intersected_ids = relation_candidates
        else:
            intersected_ids = set(self._raw_store.keys())

        # 4. FILTER & VERIFY Raw Evidences
        verified_raw: list[RawEvidenceNodeDTO] = []
        citations: list[str] = []

        for ev_id in intersected_ids:
            ev = self._raw_store.get(ev_id)
            if ev is None:
                continue

            if constraints.target_user_id and ev.user_id != constraints.target_user_id:
                continue

            verified_raw.append(ev)
            citations.append(
                f"Raw Evidence #{ev.evidence_id}: user={ev.user_id}, "
                f"session={ev.session_id}, turn={ev.turn_id}, "
                f"hash={ev.content_hash}"
            )

        verified_raw.sort(key=lambda x: x.turn_id)

        return VerifiedEvidenceBundleDTO(
            query_text=query_text,
            raw_evidences=verified_raw,
            citations=citations,
            llm_tokens_spent_indexing=0,
            llm_tokens_spent_retrieval=0,
        )
