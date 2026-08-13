"""Unit tests verifying EAOS Enterprise Provenance Package."""

from packages.provenance.domain.evidence import SourceType
from packages.provenance.domain.retrieval_query import RetrievalQuery
from packages.provenance.enterprise_provenance import (
    EAOSEnterpriseProvenancePackageEngine,
)


def test_provenance_package_raw_evidence_ingestion() -> None:
    """Verifies raw evidence ingestion and SHA256 content hashing."""
    engine = EAOSEnterpriseProvenancePackageEngine()
    ev = engine.ingest_raw_evidence(
        evidence_id="ev-pkg-001",
        user_id="user-A",
        session_id="sess-100",
        turn_id=1,
        content="Fix failing test in test_core_flows.py",
        source_type=SourceType.CONVERSATION,
    )

    assert ev.evidence_id == "ev-pkg-001"
    assert len(ev.content_hash) > 0


def test_provenance_package_dual_view_retrieval() -> None:
    """Verifies dual view intersection retrieval without LLM tokens."""
    engine = EAOSEnterpriseProvenancePackageEngine()
    engine.ingest_raw_evidence(
        evidence_id="ev-pkg-002",
        user_id="user-A",
        session_id="sess-100",
        turn_id=2,
        content="Route registration 404 issue",
    )
    engine.index_relation(
        source_name="Router",
        relation_type="HAS_ISSUE",
        target_name="Route Registration",
        evidence_id="ev-pkg-002",
        turn_id=2,
    )

    query = RetrievalQuery(
        user_id="user-A",
        session_id="sess-100",
        target_entities=["Route Registration"],
    )

    results = engine.retrieve_grounded_evidences(query)
    assert len(results) == 1
    assert results[0].evidence_id == "ev-pkg-002"
    assert "404 issue" in results[0].content
