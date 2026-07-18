import pytest
from apps.api.app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_architecture_evolution_migration_and_lineage_flow(
    client: TestClient,
) -> None:
    # 1. Khởi tạo một phiên bản gốc (v1)
    payload_1 = {
        "obj_id": "EVO-BASE-CONFIG",
        "name": "Database Schema Definition",
        "payload": {"db_port": 5432, "db_user": "eaos"},
        "author": "ArchitectAgent",
        "triggered_by": "Initial Setup",
    }
    response_1 = client.post("/evolution/propose", json=payload_1)
    assert response_1.status_code == 201
    doc_1 = response_1.json()
    assert doc_1["version"] == 1

    # 2. Thực hiện một tương thích ngược hợp lệ (Migration thành công)
    migration_payload = {
        "rules": {"db_user": "rename:postgres_user"},
        "author": "MigrationAgent",
    }
    response_migrate = client.post(
        f"/evolution/migrate/{doc_1['id']}", json=migration_payload
    )
    assert response_migrate.status_code == 200
    migrated_doc = response_migrate.json()
    assert migrated_doc["version"] == 2
    assert "postgres_user" in migrated_doc["payload"]
    assert "db_user" not in migrated_doc["payload"]

    # 3. Thử nghiệm một vi phạm tương thích ngược
    # db_port thay đổi kiểu từ int sang string -> Bắt buộc bị chặn
    invalid_migration_payload = {
        "rules": {"db_port": "default:invalid-string-port"},
        "author": "SloppyAgent",
    }
    response_invalid_migrate = client.post(
        f"/evolution/migrate/{migrated_doc['new_id']}",
        json=invalid_migration_payload,
    )
    assert response_invalid_migrate.status_code == 400
    errors = response_invalid_migrate.json()["detail"]["errors"]
    assert len(errors) > 0
    assert "Lỗi tương thích ngược" in errors[0]

    # 4. Kiểm chứng Lineage (Truy vết chuỗi gia phả ngược về gốc)
    lineage_response = client.get(f"/evolution/lineage/{migrated_doc['new_id']}")
    assert lineage_response.status_code == 200
    lineage = lineage_response.json()
    assert len(lineage) == 2
    assert lineage[0] == migrated_doc["new_id"]
    assert lineage[1] == doc_1["id"]