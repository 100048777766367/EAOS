from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class EcosystemMember(BaseModel):
    """Thực thể thành viên liên bang (Ecosystem Member - Refactored)."""

    id: str = Field(..., description="Mã định danh doanh nghiệp")
    name: str = Field(..., description="Tên doanh nghiệp")
    health_status: str = Field(
        default="HEALTHY", description="Trạng thái: HEALTHY, DEGRADED, OFFLINE"
    )
    last_heartbeat: datetime = Field(default_factory=lambda: datetime.now(UTC))
    capabilities_index: list[str] = Field(
        default_factory=list, description="Chỉ số các Năng lực cung cấp"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Siêu dữ liệu đi kèm"
    )

    model_config = ConfigDict(frozen=True)


class SharedKnowledgePacket(BaseModel):
    """Value Object đóng gói kinh nghiệm chia sẻ toàn hệ sinh thái."""

    sender_id: str = Field(..., description="Mã doanh nghiệp gửi")
    heuristic_id: str = Field(..., description="Mã quy tắc kinh nghiệm")
    rule_of_thumb: str = Field(..., description="Nội dung chỉ dẫn")
    metric_value: float = Field(..., description="Chỉ số hiệu năng kiểm định")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class FederatedCouncilVote(BaseModel):
    """Phiếu biểu quyết liên doanh nghiệp của Hội đồng liên bang."""

    voter_member_id: str = Field(..., description="Mã doanh nghiệp biểu quyết")
    voter_agent_role: str = Field(..., description="Vai trò Agent đại diện")
    decision: str = Field(..., description="APPROVED hoặc REJECTED")
    reason: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class FederatedTransaction(BaseModel):
    """Giao dịch liên bang được đồng thuận xuyên tổ chức."""

    tx_id: str
    target_ontology_id: str
    votes: list[FederatedCouncilVote] = Field(default_factory=list)
    status: str  # "APPROVED" hoặc "REJECTED"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class CollectiveEvolutionReport(BaseModel):
    """Bản ghi kết quả tiến hóa tập thể sau chẩn đoán giả lập."""

    member_id: str = Field(..., description="Mã doanh nghiệp nhận")
    received_from_id: str = Field(..., description="Mã doanh nghiệp chia sẻ")
    status: str = Field(..., description="Trạng thái: ADOPTED hoặc REJECTED")
    reason: str = Field(..., description="Lý do chốt phê duyệt")
    simulated_score: int = Field(..., description="Điểm số giả lập sau sáp nhập")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)
