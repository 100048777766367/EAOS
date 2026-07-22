from typing import Protocol

from packages.tenancy.domain.models import TenantContext


class TenantRegistryPort(Protocol):
    """Port quáº£n lÃ½ vÃ²ng Ä‘á»i vÃ  cáº¥u hÃ¬nh cá»§a cÃ¡c Tenants Ä‘á»™c láº­p."""

    def register_tenant(self, context: TenantContext) -> TenantContext: ...

    def find_by_id(self, tenant_id: str) -> TenantContext | None: ...

    def list_all(self) -> list[TenantContext]: ...
