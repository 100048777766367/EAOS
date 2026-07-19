from packages.tenancy.domain.models import TenantContext
from packages.tenancy.domain.ports import TenantRegistryPort


class InMemoryTenantRegistry(TenantRegistryPort):
    """Adapter bộ nhớ quản lý an toàn Tenant Context trong RAM."""

    def __init__(self) -> None:
        self._store: dict[str, TenantContext] = {}

    def register_tenant(self, context: TenantContext) -> TenantContext:
        self._store[context.tenant_id] = context
        return context

    def find_by_id(self, tenant_id: str) -> TenantContext | None:
        return self._store.get(tenant_id)

    def list_all(self) -> list[TenantContext]:
        return list(self._store.values())
