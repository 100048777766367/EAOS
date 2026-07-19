import hashlib
import json
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


def calculate_block_hash(
    index: int,
    previous_hash: str,
    timestamp: datetime,
    payload: dict[str, Any],
) -> str:
    """Thuật toán mã hóa băm liên kết SHA-256 bảo toàn tính toàn vẹn của khối."""
    payload_str = json.dumps(payload, sort_keys=True)
    raw = f"{index}|{previous_hash}|{timestamp.isoformat()}|{payload_str}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class CollectiveEvolutionBlock(BaseModel):
    """Khối tiến hóa mật mã toàn văn minh (Chained Block - Refactored)."""

    index: int = Field(..., description="Chỉ số khối")
    previous_hash: str = Field(..., description="Mã băm khối trước")
    current_hash: str = Field(..., description="Mã băm khối hiện tại")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    payload: dict[str, Any] = Field(..., description="Dữ liệu tiến hóa")
    signature: str = Field(..., description="Chữ ký xác minh")

    model_config = ConfigDict(frozen=True)


class AutonomousNegotiation(BaseModel):
    """Máy trạng thái thương thảo hợp đồng tự trị 5 bước."""

    id: str
    offering_member_id: str
    demanding_member_id: str
    capability_id: str
    initial_offer_tokens: float
    counter_offer_tokens: float
    status: str  # "OFFERED", "COUNTERED", "POLICY_CHECKED", "AGREED", "SETTLED"
    settlement_tx_id: str | None = Field(default=None)

    model_config = ConfigDict(frozen=True)


class FederatedCouncilVote(BaseModel):
    """Phiếu biểu quyết liên bang."""

    voter_member_id: str
    voter_agent_role: str
    decision: str
    reason: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class GlobalConsensusTransaction(BaseModel):
    """Giao dịch đồng thuận tối cao liên bang phi đồng bộ 5 bước."""

    tx_id: str
    proposal_id: str
    broadcast_topic: str
    votes: list[FederatedCouncilVote] = Field(default_factory=list)
    timeout_at: datetime
    status: str  # "PENDING", "COMMITTED", "TIMEOUT_EXPIRED", "FAILED"

    model_config = ConfigDict(frozen=True)
