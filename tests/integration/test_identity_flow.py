import uuid

import pytest
from apps.api.app.main import app, identity_repo
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_register_user_integration(client: TestClient) -> None:
    # Sinh email ngẫu nhiên để tránh lỗi trùng lặp (HTTP 400) ở các lần test sau
    test_email = f"agent.{uuid.uuid4().hex[:8]}@eaos.internal"
    
    # 1. Gọi API Đăng ký người dùng mới
    payload = {
        "email": test_email,
        "username": "AgentSmith",
        "password": "SuperSecretPassword123!"
    }
    response = client.post("/users/register", json=payload)
    
    # Kiểm tra API trả về thành công (201 Created)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["email"] == payload["email"]
    assert data["username"] == payload["username"]

    # 2. Gọi lại API với cùng email -> Phải bị chặn (HTTP 400)
    response_duplicate = client.post("/users/register", json=payload)
    assert response_duplicate.status_code == 400
    assert "already exists" in response_duplicate.json()["detail"]

    # 3. Kiểm chứng Database Adapter đã thực sự lưu dữ liệu đúng
    saved_user = identity_repo.find_by_email(payload["email"])
    assert saved_user is not None
    assert saved_user.email == payload["email"]
    
    # Đảm bảo mật khẩu ĐÃ ĐƯỢC MÃ HÓA (không lưu plaintext)
    assert saved_user.hashed_password != payload["password"]
    
    # Rút gọn bằng Tuple để qua ải Linter E501
    assert saved_user.hashed_password.startswith(("$2b$", "$2y$"))