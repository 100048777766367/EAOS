from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SemanticVersion(BaseModel):
    """Value Object định nghĩa phiên bản bất biến (Immutable Versioning)."""

    major: int = Field(default=1)
    minor: int = Field(default=0)
    patch: int = Field(default=0)
    revision: str = Field(..., description="Mã băm revision duy nhất")

    model_config = ConfigDict(frozen=True)

    def to_string(self) -> str:
        return f"v{self.major}.{self.minor}.{self.patch}-{self.revision[:6]}"


class Metadata(BaseModel):
    """Value Object quản lý thuộc tính định danh môi trường vận hành."""

    environment: str = Field(default="production")
    criticality: str = Field(default="high")
    custom_attributes: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True)


class Provenance(BaseModel):
    """Value Object mô tả chi tiết nguồn gốc biến đổi tri thức (Dòng dõi)."""

    author: str = Field(..., description="Kỹ sư hoặc AI Agent khởi tạo")
    triggered_by: str = Field(..., description="Sự kiện/Hành động kích hoạt")
    parent_id: str | None = Field(default=None, description="ID của phiên bản cha")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class Evidence(BaseModel):
    """Value Object lưu vết bằng chứng đo lường chất lượng (Fitness Score)."""

    metric_name: str = Field(..., description="Tên chỉ số kiểm định")
    metric_value: float = Field(..., description="Điểm số đạt được")
    passed: bool = Field(..., description="Độ vượt qua của ranh giới")
    log_summary: str = Field(..., description="Tóm tắt nhật ký kiểm tra")
    verified_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class RollbackSnapshot(BaseModel):
    """Snapshot bản sao lưu trữ trạng thái trước khi di chuyển (Pre-Migration)."""

    snapshot_id: str
    target_id: str
    original_payload: dict[str, Any]
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class EvolutionObject(BaseModel):
    """Aggregate Root đại diện cho đối tượng tiến hóa bất biến."""

    id: str = Field(..., description="Mã đối tượng tiến hóa")
    name: str = Field(..., description="Tên đối tượng hệ thống")
    version: SemanticVersion = Field(..., description="Phiên bản bất biến")
    payload: dict[str, Any] = Field(..., description="Cấu trúc dữ liệu")
    metadata: Metadata = Field(default_factory=Metadata)
    provenance: Provenance
    evidences: list[Evidence] = Field(default_factory=list)
    children_ids: list[str] = Field(default_factory=list)
    lineage_path: list[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


def check_backwards_compatibility(
    old_payload: dict[str, Any], new_payload: dict[str, Any]
) -> tuple[bool, list[str]]:
    """Kiểm tra tính tương thích ngược cấu trúc dữ liệu mới so với dữ liệu cũ."""
    errors = []
    for key, old_val in old_payload.items():
        if key not in new_payload:
            errors.append(f"Lỗi tương thích ngược: Khóa '{key}' bị thiếu.")
        else:
            new_val = new_payload[key]
            if type(old_val) is not type(new_val):
                errors.append(
                    f"Lỗi tương thích ngược: Khóa '{key}' thay đổi kiểu "
                    f"từ {type(old_val).__name__} sang {type(new_val).__name__}."
                )
    return len(errors) == 0, errors


def migrate_payload(
    old_payload: dict[str, Any], migration_rules: dict[str, Any]
) -> dict[str, Any]:
    """Áp dụng các quy tắc biến đổi (Migration) dữ liệu cũ sang cấu trúc mới."""
    new_payload = old_payload.copy()
    for key, action in migration_rules.items():
        if action.startswith("rename:"):
            target_key = action.split(":")[1].strip()
            if key in new_payload:
                new_payload[target_key] = new_payload.pop(key)
        elif action.startswith("default:"):
            val = action.split(":")[1].strip()
            new_payload[key] = val
    return new_payload
