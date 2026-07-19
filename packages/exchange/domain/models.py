from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class LinkedGraphNode(BaseModel):
    """Sơ đồ nút liên kết ngữ nghĩa liên doanh nghiệp bằng RDF (Sprint 3)."""

    uri: str = Field(..., description="Địa chỉ URI định danh ngữ nghĩa toàn cầu")
    relation: str = Field(..., description="Quan hệ: hasSharedPolicy, trustMember")
    target_uri: str = Field(..., description="Địa chỉ URI của nút đích")

    model_config = ConfigDict(frozen=True)


class SharedEcosystemEvent(BaseModel):
    """Sự kiện phi đồng bộ truyền phát xuyên tổ chức trên Event Mesh (Sprint 4)."""

    event_id: str
    sender_tenant_id: str
    event_type: str  # "PolicyUpdated", "CapabilityPublished"
    payload: dict[str, str]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)
