"""Master Enterprise Provenance Engine Package Orchestrator (Rule R43)."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Final

from packages.provenance.adapters.graph.relation_graph import (
    RelationGraphAdapter,
)
from packages.provenance.adapters.storage.raw_evidence_store import (
    RawEvidenceStore,
)
from packages.provenance.adapters.temporal.temporal_tree import (
    TemporalTreeAdapter,
)
from packages.provenance.domain.evidence import Evidence, SourceType
from packages.provenance.domain.retrieval_query import RetrievalQuery
from packages.provenance.retrieval.intersection import (
    DualViewIntersectionEngine,
)
from packages.provenance.retrieval.provenance_verifier import (
    ProvenanceVerifier,
)


class EAOSEnterpriseProvenancePackageEngine:
    """Master Provenance Package Orchestrator operating with 0 LLM retrieval tokens."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root: Final[Path] = (workspace_root or Path.cwd()).resolve()
        self.raw_store: Final[RawEvidenceStore] = RawEvidenceStore()
        self.graph: Final[RelationGraphAdapter] = RelationGraphAdapter()
        self.temporal: Final[TemporalTreeAdapter] = TemporalTreeAdapter()
        self.intersection_engine: Final[DualViewIntersectionEngine] = DualViewIntersectionEngine()
        self.verifier: Final[ProvenanceVerifier] = ProvenanceVerifier()

    def ingest_raw_evidence(
        self,
        evidence_id: str,
        user_id: str,
        session_id: str,
        turn_id: int,
        content: str,
        actor: str = "USER",
        source_type: SourceType = SourceType.CONVERSATION,
        source_uri: str = "",
    ) -> Evidence:
        """Ingests raw evidence and indexes into both Temporal & Relation views."""
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]

        evidence = Evidence(
            evidence_id=evidence_id,
            user_id=user_id,
            session_id=session_id,
            turn_id=turn_id,
            source_type=source_type,
            source_uri=source_uri,
            content=content,
            content_hash=content_hash,
        )
        self.raw_store.save(evidence)
        self.temporal.index_turn(
            user_id=user_id,
            session_id=session_id,
            turn_id=turn_id,
            evidence_id=evidence_id,
        )
        return evidence

    def index_relation(
        self,
        source_name: str,
        relation_type: str,
        target_name: str,
        evidence_id: str,
        turn_id: int = 1,
    ) -> None:
        """Indexes a relation view mapping pointing back to raw evidence."""
        self.graph.index_relation(
            source_name=source_name,
            relation_type=relation_type,
            target_name=target_name,
            evidence_id=evidence_id,
            turn_id=turn_id,
        )

    def retrieve_grounded_evidences(self, query: RetrievalQuery) -> list[Evidence]:
        """Executes deterministic Dual View Intersection & Provenance Verification."""
        temp_candidates = self.temporal.find_evidence_ids_by_temporal_range(
            user_id=query.user_id,
            session_id=query.session_id,
            start_turn=query.start_turn,
            end_turn=query.end_turn,
        )

        rel_candidates: set[str] = set()
        if query.target_entities:
            rel_candidates = self.graph.find_evidence_ids_by_entities(entity_names=query.target_entities)

        target_ids = self.intersection_engine.intersect_views(
            relation_candidates=rel_candidates,
            temporal_candidates=temp_candidates,
        )

        verified_results: list[Evidence] = []
        for e_id in target_ids:
            ev = self.raw_store.get_by_id(e_id)
            if ev and self.verifier.verify_evidence(ev):
                verified_results.append(ev)

        verified_results.sort(key=lambda x: x.turn_id)
        return verified_results
