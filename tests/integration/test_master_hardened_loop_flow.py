import uuid

import pytest
from apps.api.app.main import app, autonomous_repo
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.mark.anyio
async def test_master_hardened_cybernetic_loop_flow(client: TestClient) -> None:
    # 1. 13-STAGE CLOSED LOOP: Khởi chạy toàn bộ vòng lặp tự trị đóng kín thực tế từ đầu đến cuối
    loop_payload = {
        "problem": "System latency degrades under high load on Splay RAM.",
        "author": "MonitorDaemon",
    }
    response_cycle = client.post("/autonomous/run-cycle", json=loop_payload)
    assert response_cycle.status_code == 201
    cycle = response_cycle.json()
    assert cycle["status"] == "SUCCESS"
    assert "Memory" in cycle["stage_executions"]
    assert "Evolution Ledger" in cycle["stage_executions"]

    # Kiểm chứng dữ liệu đã ghi nhận thực tế vào Postgres DB
    persisted = autonomous_repo.find_by_id(cycle["cycle_id"])
    assert persisted is not None

    # 2. PLATFORM IDEMPOTENCY KEY: Chốt chặn dùng chung bảo vệ ghi trùng lặp
    idempotency_key = f"PLAT-IDEM-{uuid.uuid4().hex[:8].upper()}"
    store_payload = {
        "decision_id": "PR-2030-AUTONOMOUS-HEAL",
        "outcome": "SUCCESS",
        "evidence_summary": "Auto-remedy database port mismatch verified.",
        "lesson_learned": "Sử dụng Splay Tree giúp tự động tối ưu hóa RAM.",
        "key_learnings": ["Hot configurations nên ở gốc cây."],
    }
    resp_1 = client.post("/v1/memory/store", json={"request": store_payload, "idempotency_key": idempotency_key})
    assert resp_1.status_code == 201
    
    resp_2 = client.post("/v1/memory/store", json={"request": store_payload, "idempotency_key": idempotency_key})
    assert resp_2.status_code == 201
    assert resp_1.json()["id"] == resp_2.json()["id"]

    # 3. SEMANTIC VECTOR SEARCH (Jaccard Overlap): Tìm kiếm lọc nhiễu thông tin (Chốt > 0.15)
    # Khớp chính xác tệp lịch sử MEM-2028-FAIL chứa từ khóa "cơ sở dữ liệu"
    search_resp = client.get("/v1/memory/vector-search?query=cơ sở dữ liệu&limit=1")
    assert search_resp.status_code == 200
    assert len(search_resp.json()) == 1
    assert search_resp.json()[0]["id"] == "MEM-2028-FAIL"

    # Gửi từ khóa rác không liên quan -> Bắt buộc loại bỏ nhiễu trả về rỗng (Chống chẩn đoán sai)
    noise_resp = client.get("/v1/memory/vector-search?query=blockchain bitcoin&limit=5")
    assert noise_resp.status_code == 200
    assert len(noise_resp.json()) == 0

    # 4. FSM STUCK AUTO-RESCUE: Tự rollback cứu hộ về "rejected"
    response_start = client.post("/v1/workflows/start", json={"workflow_id": "workflow.coderagent_auto_remedy"})
    assert response_start.status_code == 201
    instance_id = response_start.json()["instance_id"]

    # Bẻ dòng dưới 100 ký tự vượt ải E501
    transition_url = "/v1/workflows/transition?simulate_stuck=true"
    resp_tx = client.post(
        transition_url,
        json={"instance_id": instance_id, "trigger": "submit"}
    )
    assert resp_tx.status_code == 200