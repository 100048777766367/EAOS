"""Domain entities and value objects for Finance bounded context."""

from pydantic import BaseModel, ConfigDict


class FinanceStatusVO(BaseModel):
    """Value object representing status of finance entity."""

    model_config = ConfigDict(frozen=True)

    status_code: str
    is_active: bool


class TokenTransactionVO(BaseModel):
    """Value object representing FinOps token transaction billing."""

    model_config = ConfigDict(frozen=True)

    transaction_id: str
    amount_usd: float
    tokens_used: int


class FinanceEntity(BaseModel):
    """Domain entity representing finance aggregate."""

    entity_id: str
    name: str
    status: FinanceStatusVO


class BillingAccountEntity(FinanceEntity):
    """Alias entity representing billing account aggregate."""
