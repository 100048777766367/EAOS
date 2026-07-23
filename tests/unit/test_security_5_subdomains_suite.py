"""Unit test suite verifying all 5 security sub-domains."""

from security.audit.zk_attestation import ZKAttestationProofEngine
from security.compliance.zero_trust_auditor import ZeroTrustAuditorEngine
from security.cryptography.post_quantum_keys import PostQuantumKeyManager
from security.identity.iam_policy import IAMPolicyEngine
from security.threats.threat_detector import ThreatDetectorEngine


def test_iam_policy_engine_rbac() -> None:
    """Verifies RBAC access evaluation."""
    engine = IAMPolicyEngine()
    assert engine.evaluate_access_permission("ADMIN", "DELETE") is True


def test_post_quantum_key_manager_fingerprint() -> None:
    """Verifies Dilithium3 key fingerprint generation."""
    mgr = PostQuantumKeyManager()
    kp = mgr.generate_key_fingerprint("key_101")
    assert "dilithium3" in kp.public_key_fingerprint


def test_zero_trust_auditor_compliance() -> None:
    """Verifies Zero-Trust compliance posture auditing."""
    auditor = ZeroTrustAuditorEngine()
    report = auditor.audit_zero_trust_posture("EAOS-SYS")
    assert report.is_compliant is True


def test_threat_detector_evaluates_ip() -> None:
    """Verifies threat detection on IP addresses."""
    detector = ThreatDetectorEngine()
    assessment = detector.evaluate_ip_threat("198.51.100.1")
    assert assessment.threat_level == 7


def test_zk_attestation_proof_verification() -> None:
    """Verifies ZK Merkle proof attestation engine."""
    engine = ZKAttestationProofEngine()
    dummy_root = "a" * 64
    proof = engine.verify_merkle_zk_proof("proof_01", dummy_root)
    assert proof.is_verified is True
