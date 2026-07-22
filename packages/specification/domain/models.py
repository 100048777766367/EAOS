from pydantic import BaseModel, ConfigDict, Field


class SpecField(BaseModel):
    """Value Object định nghĩa cấu trúc trường dữ liệu."""

    name: str
    type: str
    required: bool = True

    model_config = ConfigDict(frozen=True)


class SpecRule(BaseModel):
    """Value Object định nghĩa quy tắc nghiệp vụ đi kèm."""

    id: str
    expression: str
    error_message: str

    model_config = ConfigDict(frozen=True)


# Alias Rule sang SpecRule chống lỗi import cũ
Rule = SpecRule


class EvaluatePayloadResult(BaseModel):
    """DTO/Entity chứa kết quả thẩm định đặc tả."""

    spec_id: str
    passed: bool
    errors: list[str]

    model_config = ConfigDict(frozen=True)


class EnterpriseSpecification(BaseModel):
    """Aggregate Root đại diện cho Đặc tả doanh nghiệp hợp nhất."""

    id: str = Field(..., description="Mã đặc tả duy nhất")
    name: str = Field(..., description="Tên đặc tả thực thể")
    version: str = Field(..., description="Phiên bản đặc tả")
    fields: list[SpecField] = Field(default_factory=list)
    policies: list[str] = Field(default_factory=list)
    rules: list[SpecRule] = Field(default_factory=list)
    workflows: list[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)