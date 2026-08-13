import uuid

from packages.monetization.domain.models import TokenUsageLedgerEntry

"""Application use cases for Monetization & Token Billing."""


class BillTenantUsageUseCase:
    """Use case metering tenant API usage and issuing usage bill."""

    def execute(
        self,
        tenant_id: str,
        capability_used: str,
        prompt_tokens: int,
        completion_tokens: int,
        rate_per_k_tokens: float = 0.002,
    ) -> TokenUsageLedgerEntry:
        """Calculates usage charge and logs billing transaction."""
        tx_id = f"BILL-{uuid.uuid4().hex[:8].upper()}"
        total_tokens = prompt_tokens + completion_tokens
        charge = (total_tokens / 1000.0) * rate_per_k_tokens

        return TokenUsageLedgerEntry(
            transaction_id=tx_id,
            tenant_id=tenant_id,
            capability_used=capability_used,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            charge_usd=round(charge, 4),
            is_paid=True,
        )


if __name__ == "__main__":
    uc = BillTenantUsageUseCase()
    bill = uc.execute("TENANT_ENTERPRISE_88", "marketing", 1500, 2500)
    print(f"✔ Usage Bill Issued : {bill.transaction_id}")
    print(f"✔ Tenant ID         : {bill.tenant_id}")
    print(f"✔ Total Charge (USD): ${bill.charge_usd}")
