"""SOC Security and Quantum Signer Test Suite."""

from apps.api.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_quantum_envelope_encryption_flow() -> None:
    """Verify Post-Quantum secret payload encryption endpoint."""
    payload = {
        "secret_data": "CONFIDENTIAL_PAYLOAD_123",
        "public_key_fingerprint": "FINGERPRINT_SHA256_001",
    }
    response = client.post("/security/quantum/encrypt-envelope", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "encrypted_payload" in data or "encrypted_payload_b64" in data
    assert "algorithm" in data


def test_cloudflare_waf_ip_blocking_flow() -> None:
    """Verify Cloudflare WAF driver IP blocking endpoint."""
    response = client.post(
        "/security/cloudflare/block-ip",
        json={"ip_address": "192.168.1.100"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "BLOCKED"


def test_wazuh_siem_event_streaming_flow() -> None:
    """Verify Wazuh SIEM audit event streaming endpoint."""
    payload = {"event_id": "AUDIT-001", "severity": "HIGH"}
    response = client.post("/security/wazuh/stream-event", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "STREAMED"
