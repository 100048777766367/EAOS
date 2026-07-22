import hashlib
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


def calculate_block_hash(
    index: int,
    previous_hash: str,
    payload_summary: str = "",
    timestamp_str: str = "",
    timestamp: datetime | None = None,
    payload: dict[str, Any] | None = None,
) -> str:
    ts = timestamp_str or (timestamp.isoformat() if timestamp else "")
    ps = payload_summary or (str(payload) if payload else "")
    raw = f"{index}{previous_hash}{ps}{ts}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class AutonomousNegotiation(BaseModel):
    id: str = Field(..., description="Mã giao dịch thương thảo")
    offering_member_id: str
    demanding_member_id: str
    capability_id: str = Field(default="")
    capability_exchanged: str = Field(default="")
    initial_offer_tokens: float = Field(default=0.0)
    counter_offer_tokens: float = Field(default=0.0)
    cost_tokens: float = Field(default=0.0)
    status: str = Field(default="SETTLED")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class CollectiveEvolutionBlock(BaseModel):
    index: int
    previous_hash: str
    hash: str = Field(default="")
    current_hash: str = Field(default="")
    payload_summary: str = Field(default="")
    payload: dict[str, Any] = Field(default_factory=dict)
    signature: str = Field(default="")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class GlobalConsensusTransaction(BaseModel):
    tx_id: str
    proposal_id: str
    status: str
    committed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)
