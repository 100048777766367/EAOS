from typing import Protocol

from packages.tenancy.domain.models import TenantContext


class TenantRegistryPort(Protocol):
    """Port quản lý vòng đời và cấu hình của các Tenants độc lập."""

    def register_tenant(self, context: TenantContext) -> TenantContext: ...

    def find_by_id(self, tenant_id: str) -> TenantContext | None: ...

    def list_all(self) -> list[TenantContext]: ...
