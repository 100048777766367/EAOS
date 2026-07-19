from datetime import UTC, datetime
from pydantic import BaseModel, ConfigDict, Field


class Invoice(BaseModel):
    """Entity tự động sinh bởi Architecture Compiler."""

    id: str
    amount: float
    customer_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)

