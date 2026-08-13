from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""Accounting and Ledger Management Domain Model for EAOS."""


class GeneralLedgerRecord(BaseModel):
    """Value object representing an accounting general ledger entry."""

    model_config = ConfigDict(frozen=True)

    record_id: str = Field(..., description="Unique Record ID")
    account_code: str = Field(..., description="Chart of accounts code")
    debit_usd: float = Field(default=0.0)
    credit_usd: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
