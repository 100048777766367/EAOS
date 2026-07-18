import pytest
from apps.api.app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_assembly_and_tdo_encapsulation_flow(client: TestClient) -> None:
    # 1. Tạo tri thức mới dưới database Postgres
    payload = {
        "title": "Rule R4: Stable Core",
        "content": "Hiến pháp kiến trúc lõi cứng v4.0",
        "author": "Chief Architect",
    }
    response = client.post("/knowledge", json=payload)
    assert response.status_code == 201
    doc_id = response.json()["id"]

    # 2. Gửi yêu cầu lên Hội đồng để kiểm duyệt, biểu quyết và xuất tệp đóng gói TDO
    assembly_payload = {
        "artifact_id": doc_id,
        "action": "ADD",
        "author": "Solopreneur",
    }
    assembly_response = client.post(
        "/governance/assembly/commit", json=assembly_payload
    )
    assert assembly_response.status_code == 201
    result = assembly_response.json()

    # Kiểm duyệt giao dịch được đóng gói thành công
    assert result["transaction"]["status"] == "COMMITTED"
    assert result["transaction"]["artifact_id"] == doc_id

    # Đảm bảo TDO tự mô tả có chứa mã băm Fixity bảo mật toàn vẹn
    tdo = result["trustworthy_digital_object"]
    assert tdo["@context"] == "https://eaos.internal/contexts/governance.jsonld"
    assert tdo["data"]["id"] == doc_id
    assert tdo["fixity"]["value"] is not None