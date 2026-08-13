"""Tenancy and Metering Router."""

from typing import Annotated, Any

from fastapi import APIRouter, Body
from packages.tenancy.infrastructure.rls_adapter import RLSContextDTO
from packages.tenancy.infrastructure.tenant_metering import (
    TenantMeteringGuard,
    TenantQuotaCheck,
)

from apps.api.app.container import rls_adapter

router = APIRouter(prefix="/tenancy", tags=["Tenancy"])


@router.post("/rls/apply-context", response_model=RLSContextDTO)
async def apply_tenant_rls_context(
    request: dict[str, Any] | None = None,
    tenant_id: Annotated[str | None, Body(embed=True)] = None,
) -> RLSContextDTO:
    t_id = tenant_id
    if not t_id and isinstance(request, dict):
        t_id = str(request.get("tenant_id", "default_tenant"))
    return rls_adapter.apply_tenant_rls_context(t_id or "default_tenant")


@router.post("/metering/enforce")
async def enforce_tenant_metering(
    request: dict[str, Any] | None = None,
    tenant_id: Annotated[str | None, Body(embed=True)] = None,
    resource_type: Annotated[str | None, Body(embed=True)] = None,
    limit: Annotated[float | None, Body(embed=True)] = None,
) -> TenantQuotaCheck:
    t_id = tenant_id
    r_type = resource_type
    lim = limit
    if isinstance(request, dict):
        if not t_id:
            t_id = str(request.get("tenant_id", "default_tenant"))
        if not r_type:
            r_type = str(request.get("resource_type", "llm_tokens"))
        if lim is None:
            lim = float(request.get("limit", 1000.0))

    guard = TenantMeteringGuard()
    return guard.check_quota(
        tenant_id=t_id or "default_tenant",
        resource_type=r_type or "llm_tokens",
        limit=lim if lim is not None else 1000.0,
    )
