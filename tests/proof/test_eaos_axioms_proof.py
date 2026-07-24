"""Proof test suite verifying the 6 Constitutional Axioms of EAOS."""

from tools.proof.proof_engine import EAOSAxiomsProofEngine


def test_eaos_6_constitutional_axioms_proof() -> None:
    """Empirically proves the 6 core claims of EAOS Architecture."""
    engine = EAOSAxiomsProofEngine()
    results = engine.prove_all_axioms()

    assert len(results) == 6
    assert all(r.is_proven for r in results)
    assert all(r.metrics_score == 100.0 for r in results)
