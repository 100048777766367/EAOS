from pydantic import BaseModel

from packages.tenancy.domain.models import TenantContext, TenantPolicyOverride
from packages.tenancy.domain.ports import TenantRegistryPort


class CreateTenantRequest(BaseModel):
    tenant_id: str
    domain_name: str
    capabilities: list[str]


class RegisterTenantUseCase:
    """Application Service điều phối cấu hình cô lập cho doanh nghiệp mới."""

    def __init__(self, registry: TenantRegistryPort) -> None:
        self.registry = registry

    def execute(self, request: CreateTenantRequest) -> TenantContext:
        # Tự động nạp chính sách bảo mật mặc định cho Tenant
        default_override = TenantPolicyOverride(
            policy_id="P-001-retention-compaction",
            is_enabled=True,
            override_details={"max_active_nodes": "500"},
        )
        context = TenantContext(
            tenant_id=request.tenant_id,
            domain_name=request.domain_name,
            activated_capabilities=request.capabilities,
            policy_overrides=[default_override],
        )
        return self.registry.register_tenant(context)
