import pytest
from apps.api.app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_complete_evolution_lifecycle_sprints_3_to_6(
    client: TestClient,
) -> None:
    # --- SPRINT 1-2: Đề xuất cấu hình ban đầu ---
    payload = {
        "obj_id": "EVO-SELF-HEAL-CONFIG",
        "name": "Self Healing Target System",
        "payload": {"max_retry_loops": 10, "llm_fallback": "gpt-4"},
        "author": "ArchitectAgent",
        "triggered_by": "Initial Setup",
    }
    response_init = client.post("/evolution/propose", json=payload)
    assert response_init.status_code == 201
    doc_id = response_init.json()["id"]

    # --- SPRINT 3: Chạy Fitness Engine & Rules Engine đánh giá chất lượng ---
    fitness_resp = client.post(f"/evolution/evaluate-fitness/{doc_id}")
    assert fitness_resp.status_code == 200
    fitness_data = fitness_resp.json()
    assert fitness_data["passed"] is True
    assert fitness_data["fitness_score"] == 1.0

    # --- SPRINT 4: Hội đồng biểu quyết (Consensus Voting) & Ghi sổ Ledger ---
    votes = [
        {"voter": "ArchitectAgent", "decision": "APPROVED", "reason": "OK"},
        {"voter": "ReviewerAgent", "decision": "APPROVED", "reason": "Clear"},
    ]
    vote_resp = client.post(
        f"/evolution/council/vote/{doc_id}", json={"voters_payload": votes}
    )
    assert vote_resp.status_code == 200
    tx = vote_resp.json()["transaction"]
    assert tx["status"] == "APPROVED"

    # --- SPRINT 5: Biên dịch ngữ nghĩa (Semantic JSON-LD & RDF Triples) ---
    semantic_resp = client.get(f"/evolution/semantic/{doc_id}")
    assert semantic_resp.status_code == 200
    semantic_data = semantic_resp.json()
    assert semantic_data["json_ld"]["@type"] == "eaos:EvolutionObject"
    assert len(semantic_data["rdf_triples"]) > 0

    # --- SPRINT 6: Kích hoạt tự thích ứng và khắc phục lỗi (Self-healing) ---
    heal_resp = client.post(f"/evolution/self-heal/{doc_id}")
    assert heal_resp.status_code == 200
    healed_data = heal_resp.json()
    # Kiểm chứng payload đã tự thích ứng giảm max_retry_loops từ 10 xuống 5 (10 * 0.5)
    assert healed_data["payload"]["max_retry_loops"] == 5.0
    assert healed_data["payload"]["llm_fallback"] == "local-llama"