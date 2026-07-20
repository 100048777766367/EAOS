from pydantic import BaseModel, ConfigDict, Field


class Rule(BaseModel):
    """Quy tắc kiểm duyệt thực thể nghiệp vụ."""

    id: str
    expression: str
    error_message: str

    model_config = ConfigDict(frozen=True)


class EnterpriseSpecification(BaseModel):
    """Đặc tả thực thể doanh nghiệp tự trị (Invoice, Customer...)."""

    id: str
    name: str
    rules: list[Rule] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)