import pytest
from apps.api.app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_master_evolution_and_self_healing_flow(client: TestClient) -> None:
    # 1. PROPOSE & COUNCIL VOTE: Đề xuất phiên bản bất biến và bỏ phiếu thông qua
    payload_init = {
        "obj_id": "EVO-ALL-FLOW-TARGET",
        "name": "Auto Remediation Module",
        "payload": {"max_retry_loops": 10, "llm_fallback": "gpt-4", "__version": 1},
        "author": "ArchitectAgent",
        "triggered_by": "Initial Setup",
        "voters_payload": [{"voter": "ArchitectAgent", "decision": "APPROVED", "reason": "Compliant"}],
    }
    response_1 = client.post("/evolution/propose", json=payload_init)
    assert response_1.status_code == 201
    doc_1 = response_1.json()
    assert doc_1["version"].startswith("v1.0.0")

    # 2. RUN FITNESS: Thẩm định quy tắc hiến pháp chỉ số thể lực
    fitness_resp = client.post(f"/evolution/evaluate-fitness/{doc_1['id']}")
    assert fitness_resp.status_code == 200
    assert fitness_resp.json()["passed"] is True
    assert fitness_resp.json()["fitness_score"] == 1.0

    # 3. REFLECTION & LEARNING: Chẩn đoán nguyên nhân sự cố và tự động nạp Kinh nghiệm vào RAM cache
    ref_response = client.post(
        "/reflection/analyze",
        json={"subject_id": doc_1["id"], "trigger_event": "Fitness Failure", "passed_checks": False},
    )
    assert ref_response.status_code == 201
    ref_id = ref_response.json()["id"]

    learn_response = client.post("/learning/ingest", json={"reflection_id": ref_id})
    assert learn_response.status_code == 201
    assert learn_response.json()["id"].startswith("EXP-")

    # 4. SELF-REWRITE & METADATA SNAPSHOT ROLLBACK: Di chuyển cấu trúc an toàn, rollback nếu vi phạm
    # Thử nghiệm di chuyển vi phạm tương thích ngược (db_port thay đổi kiểu) -> Phải tự kích hoạt Auto-Rollback
    migration_payload = {"rules": {"db_port": "default:invalid-port"}, "author": "SloppyAgent"}
    response_invalid = client.post(f"/evolution/migrate/{doc_1['id']}", json=migration_payload)
    assert response_invalid.status_code == 400
    assert "Đã Rollback về Snapshot" in response_invalid.json()["detail"]

    # 5. AGENT CHAIN SELF-REWRITE: AI tự động lập trình và tạo Pull Request chứa file Patch sạch
    payload_rewrite = {
        "problem": "Database port mismatch causing connection timeouts.",
        "author": "SystemMonitor",
    }
    rewrite_resp = client.post("/v1/self-rewrite/run", json=payload_rewrite)
    assert rewrite_resp.status_code == 201
    job = rewrite_resp.json()
    assert job["status"] == "SUCCESS"
    assert len(job["agent_logs"]) == 5
    assert job["pull_request"]["target_branch"] == "main"