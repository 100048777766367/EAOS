import json
import os
from datetime import UTC, datetime
from typing import Any  # <-- THÊM ĐÚNG IMPORT ANY VÀO ĐÂY

from pydantic import BaseModel, Field

from packages.evolution.domain.models import EvolutionObject


class CouncilVote(BaseModel):
    """Lá phiếu biểu quyết của Hội đồng quản trị Agent/Con người."""

    voter: str
    decision: str  # "APPROVED" hoặc "REJECTED"
    reason: str
    voted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class EvolutionTransaction(BaseModel):
    """Giao dịch tiến hóa đã được phê duyệt và ghi sổ."""

    tx_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    evolution_id: str
    votes: list[CouncilVote]
    status: str  # "APPROVED" hoặc "REJECTED"


class EvolutionGovernanceCouncil:
    """Hội đồng giám sát biểu quyết cho các đề xuất tự tiến hóa."""

    def __init__(
        self, ledger_path: str = "runtime/traces/evolution_ledger.jsonl"
    ) -> None:
        self.ledger_path = ledger_path
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)

    def evaluate_proposal(
        self, obj: EvolutionObject, votes: list[CouncilVote]
    ) -> EvolutionTransaction:
        import uuid

        approved_voters = [v for v in votes if v.decision == "APPROVED"]
        passed = len(approved_voters) >= (len(votes) / 2)

        status = "APPROVED" if passed else "REJECTED"
        tx_id = f"TX-EVO-{uuid.uuid4().hex[:8].upper()}"

        tx = EvolutionTransaction(
            tx_id=tx_id,
            evolution_id=obj.id,
            votes=votes,
            status=status,
        )

        with open(self.ledger_path, "a", encoding="utf-8") as f:
            f.write(tx.model_dump_json() + "\n")

        return tx

    def list_transactions(self) -> list[dict[str, Any]]:
        if not os.path.exists(self.ledger_path):
            return []
        with open(self.ledger_path, encoding="utf-8") as f:
            return [json.loads(line.strip()) for line in f if line.strip()]