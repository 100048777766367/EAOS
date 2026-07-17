import pytest
from apps.api.app.main import app, knowledge_repo
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_store_and_retrieve_knowledge_integration(client: TestClient) -> None:
    # 1. Gửi request lưu trữ dữ liệu thông qua FastAPI Endpoint
    payload = {
        "title": "EAOS Architecture Constitution",
        "content": "Rule R4: Stable Core, Flexible Edge",
        "author": "Chief Architect",
    }
    response = client.post("/knowledge", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["title"] == payload["title"]

    # 2. Kiểm chứng Database Adapter đã thực sự lưu thông tin vào Postgres container
    artifact_id = data["id"]
    saved_artifact = knowledge_repo.find_by_id(artifact_id)

    assert saved_artifact is not None
    assert saved_artifact.content == payload["content"]