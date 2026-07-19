import pytest
from apps.api.app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_master_ecosystem_multi_tenant_and_civilization_flow(client: TestClient) -> None:
    # 1. CAPABILITY & SPECIFICATION
    valid_payload = {
        "spec_id": "spec.invoice",
        "payload": {
            "id": "INV-1001",
            "amount": 1500.0,
            "customer_id": "CUST-99"
        }
    }
    # Bẻ dòng dưới 100 ký tự vượt ải E501
    response_valid = client.post(
        "/v1/specifications/evaluate", json=valid_payload
    )
    assert response_valid.status_code == 200
    assert response_valid.json()["passed"] is True

    # 2. SERVICE DISCOVERY (Registry)
    response_registry = client.get("/v1/registry")
    assert response_registry.status_code == 200
    assert len(response_registry.json()) >= 4

    # 3. TENANCY (Multi-Tenant Runtime)
    tenant_payload = {
        "tenant_id": "Tenant-C",
        "domain_name": "tenant-c.eaos.internal",
        "capabilities": ["capability.identity"]
    }
    # Bẻ dòng dưới 100 ký tự vượt ải E501
    response_tenant = client.post(
        "/v1/tenancy/register", json=tenant_payload
    )
    assert response_tenant.status_code == 201

    # 4. DISTRIBUTED EVENT MESH (Exchange)
    event_payload = {
        "event_id": "EV-DIST-100",
        "topic": "governance.ontology",
        "correlation_id": "TX-CORR-100",
        "trace_id": "TRC-999",
        "sequence_number": 1,
        "sender_tenant_id": "Enterprise-A",
        "event_type": "PolicyUpdated",
        "payload": {"status": "SUCCESS"},
    }
    response_evt = client.post("/v1/exchange/broadcast", json=event_payload)
    assert response_evt.status_code == 201

    # 5. MARKETPLACE
    asset_payload = {
        "asset_id": "asset.finance",
        "name": "Finance Capability",
        "category": "CAPABILITY",
        "manifest_payload": {"version": "1.0.0", "db": "postgres"},
        "publisher_id": "Enterprise-A",
    }
    response_asset = client.post("/v1/marketplace/publish", json=asset_payload)
    assert response_asset.status_code == 201

    # 6. AUTONOMOUS NEGOTIATION (5 Bước)
    neg_payload = {
        "offering_member_id": "Enterprise-A",
        "demanding_member_id": "Enterprise-B",
        "capability_exchanged": "capability.identity",
        "cost_tokens": 1000.0,
    }
    resp_neg = client.post("/v1/civilization/negotiate", json=neg_payload)
    assert resp_neg.status_code == 201
    neg_data = resp_neg.json()
    assert neg_data["status"] == "SETTLED"
    assert neg_data["settlement_tx_id"].startswith("SETTLE-TX-")

    # 7. GLOBAL CONSENSUS & LEDGER CHAIN (Genesis -> Block1)
    consensus_payload = {"proposal_id": neg_data["id"], "approvals_count": 2, "total_participants": 2}
    resp_con = client.post("/v1/civilization/consensus", json=consensus_payload)
    assert resp_con.status_code == 201
    assert resp_con.json()["status"] == "COMMITTED"

    blocks_resp = client.get("/v1/civilization/blocks")
    assert blocks_resp.status_code == 200
    blocks = blocks_resp.json()
    assert len(blocks) == 2
    assert blocks[0]["index"] == 0
    assert blocks[1]["index"] == 1
    assert blocks[1]["previous_hash"] == blocks[0]["current_hash"]