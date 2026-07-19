from pydantic import BaseModel, ConfigDict, Field


class SpecField(BaseModel):
    """Value Object định nghĩa cấu trúc trường dữ liệu (Schema Field)."""

    name: str
    type: str  # "str", "float", "int"
    required: bool = True

    model_config = ConfigDict(frozen=True)


class SpecRule(BaseModel):
    """Value Object định nghĩa quy tắc nghiệp vụ đi kèm (Business Rule)."""

    id: str
    expression: str
    error_message: str

    model_config = ConfigDict(frozen=True)


class EnterpriseSpecification(BaseModel):
    """Aggregate Root đại diện cho Đặc tả doanh nghiệp hợp nhất (Spec)."""

    id: str = Field(..., description="Mã đặc tả duy nhất (spec.invoice)")
    name: str = Field(..., description="Tên đặc tả thực thể")
    version: str = Field(..., description="Phiên bản đặc tả")
    fields: list[SpecField] = Field(default_factory=list)
    policies: list[str] = Field(default_factory=list)
    rules: list[SpecRule] = Field(default_factory=list)
    workflows: list[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)
