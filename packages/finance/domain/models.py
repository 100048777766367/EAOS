from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""Finance & FinOps Domain Model for EAOS Capability App."""


class FinancialLedgerEntry(BaseModel):
    """Value object representing a financial transaction."""

    model_config = ConfigDict(frozen=True)

    transaction_id: str = Field(..., description="Unique Tx ID")
    revenue_usd: float = Field(default=0.0)
    cost_usd: float = Field(default=0.0)
    net_margin_usd: float = Field(default=0.0)
    entry_type: str = Field(default="AFFILIATE_PAYOUT")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @property
    def entity_id(self) -> str:
        """Alias for entity identifier compatibility."""
        return self.transaction_id


# Alias for legacy infrastructure adapters compatibility
FinanceEntity = FinancialLedgerEntry
