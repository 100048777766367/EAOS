from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class TenantPolicyOverride(BaseModel):
    """Value Object quáº£n lÃ½ viá»‡c ghi Ä‘Ã¨ Policy Ä‘áº·c thÃ¹ cá»§a tá»«ng Doanh nghiá»‡p."""

    policy_id: str
    is_enabled: bool = True
    override_details: dict[str, str] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True)


class TenantContext(BaseModel):
    """Aggregate Root quáº£n lÃ½ ngá»¯ cáº£nh an toÃ n cá»§a tá»«ng doanh nghiá»‡p cÃ´ láº­p."""

    tenant_id: str = Field(..., description="MÃ£ phÃ¢n má»¥c doanh nghiá»‡p")
    domain_name: str = Field(..., description="TÃªn miá»n doanh nghiá»‡p")
    activated_capabilities: list[str] = Field(default_factory=list)
    policy_overrides: list[TenantPolicyOverride] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)

