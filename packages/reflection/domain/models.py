from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class RootCause(BaseModel):
    """Mô tả chi tiết nguyên nhân gốc rễ gây ra sụt giảm chỉ số thể lực."""

    id: str = Field(..., description="Mã nguyên nhân")
    type: str = Field(..., description="Phân loại nguyên nhân lỗi")
    description: str = Field(..., description="Mô tả chi tiết sự cố")
    probability: float = Field(..., description="Xác suất chính xác (0.0-1.0)")
    evidence: list[str] = Field(default_factory=list, description="Bằng chứng")

    model_config = ConfigDict(frozen=True)


class Recommendation(BaseModel):
    """Khuyến nghị hành động khắc phục lỗi được đề xuất bởi Reflection."""

    priority: str = Field(..., description="Mức độ ưu tiên (HIGH/MEDIUM/LOW)")
    action: str = Field(..., description="Hành động sửa đổi cần thực hiện")
    reason: str = Field(..., description="Lý do đề xuất")
    risk: str = Field(..., description="Rủi ro đi kèm khi thực thi")

    model_config = ConfigDict(frozen=True)


class ReflectionReport(BaseModel):
    """Báo cáo tự suy ngẫm và chẩn đoán sự cố hoàn chỉnh của EAOS."""

    id: str = Field(..., description="Mã báo cáo duy nhất")
    subject: str = Field(..., description="Mã đối tượng kiểm tra (artifact_id)")
    trigger: str = Field(..., description="Sự kiện kích hoạt (Fitness Fail)")
    root_causes: list[RootCause] = Field(default_factory=list)
    confidence: float = Field(..., description="Độ tự tin của báo cáo")
    recommendations: list[Recommendation] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)