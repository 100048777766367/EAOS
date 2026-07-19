from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskNode(BaseModel):
    """Nút đại diện cho một tác vụ tự trị (Task Node) [2]."""

    id: str = Field(..., description="Mã tác vụ")
    name: str = Field(..., description="Tên tác vụ")
    status: str = Field(default="PENDING", description="Trạng thái thực thi")

    model_config = ConfigDict(frozen=True)


class Confidence(BaseModel):
    """Điểm số tự tin kiểm duyệt chẩn đoán."""

    score: float = Field(default=1.0, description="Điểm tin cậy từ 0.0-1.0")
    reason: str = Field(default="Phân tích logic đạt chuẩn", description="Lý giải")

    model_config = ConfigDict(frozen=True)


class ReasoningNode(BaseModel):
    """Value Object định nghĩa một nút suy luận ngữ nghĩa của AI."""

    id: str
    premise: str = Field(..., description="Tiền đề sự cố")
    deduction: str = Field(..., description="Suy luận logic rút ra")
    confidence: float = Field(default=1.0, description="Độ tự tin")

    model_config = ConfigDict(frozen=True)


class EcosystemPlan(BaseModel):
    """Aggregate Root đại diện cho Kế hoạch tự trị phân phối toàn liên bang."""

    id: str = Field(..., description="Mã kế hoạch")
    steps: list[str] = Field(default_factory=list, description="Các bước")
    assigned_agent: str = Field(..., description="AI Agent chịu trách nhiệm")
    duration_ms: float = Field(default=0.0, description="Thời gian thực thi")

    model_config = ConfigDict(frozen=True)


class OptimizationGoal(BaseModel):
    """Value Object quản lý việc Tối ưu hóa chỉ số tự trị (Autonomous Optimization)."""

    target_metric: str = Field(..., description="Tên chỉ số cần tối ưu")
    target_value: float = Field(..., description="Chỉ số kỳ vọng đạt được")
    current_value: float = Field(..., description="Chỉ số thực tế hiện tại")
    adjustments_applied: dict[str, float] = Field(
        default_factory=dict, description="Các tham số đã tự động tinh chỉnh"
    )

    model_config = ConfigDict(frozen=True)


class SemanticDecision(BaseModel):
    """Thực thể Quyết định tự trị có căn cứ khoa học của hệ điều hành."""

    id: str = Field(..., description="Mã quyết định")
    chosen_option: str = Field(..., description="Phương án được phê duyệt")
    rationale: str = Field(..., description="Cơ sở lý giải logic")
    confidence_score: float = Field(..., description="Điểm tin cậy tối cao")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)