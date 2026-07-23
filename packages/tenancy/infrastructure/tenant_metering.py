"""Tenant resource metering and quota enforcement guard for EAOS multi-tenancy."""

from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class TenantQuotaCheck(BaseModel):
    """Value object representing tenant quota enforcement check results."""

    model_config = ConfigDict(frozen=True)

    tenant_id: str
    allowed: bool
    current_usage: float
    max_limit: float
    reason: str


class TenantMeteringGuard:
    """Tracks tenant resource consumption and enforces allocation quotas."""

    _usage_ledger: ClassVar[dict[str, dict[str, float]]] = {}

    def record_usage(
        self,
        tenant_id: str,
        resource_type: str,
        amount: float,
    ) -> None:
        """Records cumulative resource consumption for a given tenant."""
        if tenant_id not in self._usage_ledger:
            self._usage_ledger[tenant_id] = {}
        curr = self._usage_ledger[tenant_id].get(resource_type, 0.0)
        self._usage_ledger[tenant_id][resource_type] = curr + amount

    def check_quota(
        self,
        tenant_id: str,
        resource_type: str,
        limit: float,
    ) -> TenantQuotaCheck:
        """Evaluates current usage against limit to determine allowance."""
        tenant_usage = self._usage_ledger.get(tenant_id, {})
        current_amount = tenant_usage.get(resource_type, 0.0)

        if current_amount > limit:
            return TenantQuotaCheck(
                tenant_id=tenant_id,
                allowed=False,
                current_usage=current_amount,
                max_limit=limit,
                reason=(f"Quota exceeded for '{resource_type}'. Used {current_amount} > Limit {limit}"),
            )

        return TenantQuotaCheck(
            tenant_id=tenant_id,
            allowed=True,
            current_usage=current_amount,
            max_limit=limit,
            reason=f"Usage within allocated limit for '{resource_type}'.",
        )
