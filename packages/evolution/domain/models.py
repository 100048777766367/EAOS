from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SemanticVersion(BaseModel):
    major: int = Field(default=1)
    minor: int = Field(default=0)
    patch: int = Field(default=0)
    revision: str = Field(default="REV-INIT")

    def to_string(self) -> str:
        return f"v{self.major}.{self.minor}.{self.patch}-{self.revision}"

    model_config = ConfigDict(frozen=True)


class Metadata(BaseModel):
    environment: str = Field(default="production")
    criticality: str = Field(default="high")
    custom_attributes: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True)


class Provenance(BaseModel):
    author: str = Field(..., description="Tác giả")
    triggered_by: str = Field(..., description="Sự kiện")
    parent_id: str | None = Field(default=None)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class Evidence(BaseModel):
    metric_name: str
    metric_value: float
    passed: bool
    log_summary: str
    verified_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class RollbackSnapshot(BaseModel):
    snapshot_id: str
    target_id: str
    version_tag: str
    payload_backup: dict[str, Any] = Field(default_factory=dict)
    original_payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class EvolutionObject(BaseModel):
    id: str
    name: str
    version: SemanticVersion = Field(
        default_factory=lambda: SemanticVersion(major=1, minor=0, patch=0, revision="REV-INIT")
    )
    payload: dict[str, Any]
    metadata: Metadata = Field(default_factory=Metadata)
    provenance: Provenance
    evidences: list[Evidence] = Field(default_factory=list)

    model_config = ConfigDict(arbitrary_types_allowed=True)


def check_backwards_compatibility(old_payload: dict[str, Any], new_payload: dict[str, Any]) -> tuple[bool, list[str]]:
    errors = []
    for key, old_val in old_payload.items():
        if key == "__version":
            continue
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


def migrate_payload(old_payload: dict[str, Any], migration_rules: dict[str, Any]) -> dict[str, Any]:
    new_payload = old_payload.copy()
    for key, action in migration_rules.items():
        if action.startswith("rename:"):
            target_key = action.split(":")[1].strip()
            if key in new_payload:
                new_payload[target_key] = new_payload.pop(key)
        elif action.startswith("default:"):
            raw_val = action.split(":")[1].strip()
            if key in old_payload:
                old_type = type(old_payload[key])
                if old_type is int:
                    try:
                        new_payload[key] = int(raw_val)
                    except ValueError:
                        new_payload[key] = raw_val
                elif old_type is float:
                    try:
                        new_payload[key] = float(raw_val)
                    except ValueError:
                        new_payload[key] = raw_val
                else:
                    new_payload[key] = raw_val
            else:
                new_payload[key] = raw_val
    return new_payload
