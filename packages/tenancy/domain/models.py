from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class TenantPolicyOverride(BaseModel):
    """Value Object quản lý việc ghi đè Policy đặc thù của từng Doanh nghiệp."""

    policy_id: str
    is_enabled: bool = True
    override_details: dict[str, str] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True)


class TenantContext(BaseModel):
    """Aggregate Root quản lý ngữ cảnh an toàn của từng doanh nghiệp cô lập."""

    tenant_id: str = Field(..., description="Mã phân mục doanh nghiệp")
    domain_name: str = Field(..., description="Tên miền doanh nghiệp")
    activated_capabilities: list[str] = Field(default_factory=list)
    policy_overrides: list[TenantPolicyOverride] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)
