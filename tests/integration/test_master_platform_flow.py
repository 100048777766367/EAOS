import uuid
from pathlib import Path

import pytest
from apps.api.app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_master_platform_and_lifecycle_flow(client: TestClient) -> None:
    # 1. IDENTITY
    test_email = f"agent.{uuid.uuid4().hex[:8]}@eaos.internal"
    payload_user = {
        "email": test_email,
        "username": "AgentSmith",
        "password": "SuperSecretPassword123!",
    }
    resp_user = client.post("/users/register", json=payload_user)
    assert resp_user.status_code == 201
    user_data = resp_user.json()
    assert user_data["id"] is not None

    resp_dup = client.post("/users/register", json=payload_user)
    assert resp_dup.status_code == 400

    # 2. SPLAY CACHE
    payload_knw = {
        "title": "Rule R4: Stable Core",
        "content": "Hiến pháp bảo vệ nhân nghiệp vụ an toàn.",
        "author": "Chief Architect",
    }
    resp_knw = client.post("/knowledge", json=payload_knw)
    assert resp_knw.status_code == 201
    knw_id = resp_knw.json()["id"]

    # 3. TDO & ASSEMBLY
    assembly_payload = {
        "artifact_id": knw_id,
        "action": "ADD",
        "author": "Solopreneur",
    }
    resp_commit = client.post(
        "/governance/assembly/commit", json=assembly_payload
    )
    assert resp_commit.status_code == 201
    commit_data = resp_commit.json()
    assert commit_data["transaction"]["status"] == "COMMITTED"
    assert (
        commit_data["trustworthy_digital_object"]["@context"]
        == "https://eaos.internal/contexts/governance.jsonld"
    )

    # 4. WORKFLOW FSM
    response_start = client.post(
        "/v1/workflows/start",
        json={"workflow_id": "workflow.invoice_approval"},
    )
    assert response_start.status_code == 201
    instance_id = response_start.json()["instance_id"]

    response_tx = client.post(
        "/v1/workflows/transition",
        json={"instance_id": instance_id, "trigger": "submit"},
    )
    assert response_tx.status_code == 200
    assert response_tx.json()["current_state"] == "validating"

    # 5. DLM (Sửa dòng dài vượt ải E501)
    ROOT_PATH = Path(__file__).resolve().parent.parent.parent
    mock_file = ROOT_PATH / "docs" / "mock_system_constitution.md"
    roadmap_file = ROOT_PATH / "docs" / "ROADMAP.md"
    target_doc = mock_file if mock_file.exists() else roadmap_file

    from engine.compiler.document_lifecycle_controller import (
        DocumentLifecycleController,
    )

    dlm_controller = DocumentLifecycleController(ROOT_PATH)
    success_dlm = dlm_controller.transition_state(
        doc_path=target_doc,
        target_status="SUSPENDED",
        reason="Ecosystem hardlock active",
    )
    assert success_dlm is True