"""Unit test suite for EAOS security domain architecture."""

from pathlib import Path

from security.cryptography.post_quantum_keys import (
    PostQuantumKeyManager,
)
from security.security_engine import EnterpriseSecurityEngine
from security.threats.threat_detector import ThreatDetectorEngine

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_enterprise_security_engine_audits_5_domains() -> None:
    """Verifies enterprise security engine audits all 5 sub-domains."""
    engine = EnterpriseSecurityEngine(ROOT_PATH)
    audits = engine.audit_security_architecture()
    assert len(audits) == 5
    domains = {a.domain for a in audits}
    assert "identity" in domains
    assert "cryptography" in domains
    assert "compliance" in domains
    assert "threats" in domains
    assert "audit" in domains


def test_post_quantum_key_manager() -> None:
    """Verifies post-quantum Dilithium3 key fingerprint generation."""
    mgr = PostQuantumKeyManager()
    kp = mgr.generate_key_fingerprint("key_001")
    assert "dilithium3" in kp.public_key_fingerprint
    assert kp.key_length_bits == 2560


def test_threat_detector_engine() -> None:
    """Verifies SOC threat detection and WAF action recommendation."""
    detector = ThreatDetectorEngine()
    res = detector.evaluate_ip_threat("198.51.100.25")
    assert res.threat_level == 7
    assert res.mitigation_action == "BLOCK_WITH_COOLDOWN"
