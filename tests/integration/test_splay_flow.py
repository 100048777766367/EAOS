import pytest
from apps.api.app.main import app, knowledge_repo
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_splay_and_logging_integration_flow(client: TestClient) -> None:
    # 1. Gửi request lưu trữ dữ liệu thông qua FastAPI Endpoint
    payload_1 = {
        "title": "Rule R1: Stable Core",
        "content": "Hiến pháp kiến trúc lõi cứng",
        "author": "Chief Architect",
    }
    response_1 = client.post("/knowledge", json=payload_1)
    assert response_1.status_code == 201
    doc_1_id = response_1.json()["id"]

    # 2. Tạo tiếp tài liệu thứ hai -> Splay lên Root
    payload_2 = {
        "title": "Rule R2: Flexible Edge",
        "content": "Giao diện phân phối mềm dẻo",
        "author": "Architect Agent",
    }
    response_2 = client.post("/knowledge", json=payload_2)
    assert response_2.status_code == 201
    doc_2_id = response_2.json()["id"]

    # 3. Root của Splay Tree bắt buộc phải là DOC-02
    tree_response = client.get("/governance/splay-tree")
    assert tree_response.status_code == 200
    layout = tree_response.json()["root"]
    # Sửa lỗi: Truy cập trực tiếp vào khóa "key" của layout
    assert layout["key"] == doc_2_id

    # 4. Kích hoạt đọc lại tài liệu thứ nhất (DOC-01) -> Splay lên làm Root mới
    saved_doc_1 = knowledge_repo.find_by_id(doc_1_id)
    assert saved_doc_1 is not None

    # Đọc lại cấu trúc cây. Lúc này DOC-01 phải nhảy lên làm Root mới
    tree_response_updated = client.get("/governance/splay-tree")
    assert tree_response_updated.status_code == 200
    layout_updated = tree_response_updated.json()["root"]
    # Sửa lỗi: Truy cập trực tiếp vào khóa "key" của layout_updated
    assert layout_updated["key"] == doc_1_id

    # 5. Kiểm tra nhật ký thay đổi (Audit Log)
    audit_response = client.get(f"/governance/audit-logs/{doc_1_id}")
    assert audit_response.status_code == 200
    logs = audit_response.json()
    assert len(logs) == 1
    assert logs[0]["action"] == "ADD"