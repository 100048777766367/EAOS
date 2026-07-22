import json
import os
from datetime import UTC, datetime
from typing import Any  # <-- THÃŠM ÄÃšNG IMPORT ANY VÃ€O ÄÃ‚Y

from pydantic import BaseModel, Field

from packages.evolution.domain.models import EvolutionObject


class CouncilVote(BaseModel):
    """LÃ¡ phiáº¿u biá»ƒu quyáº¿t cá»§a Há»™i Ä‘á»“ng quáº£n trá»‹ Agent/Con ngÆ°á»i."""

    voter: str
    decision: str  # "APPROVED" hoáº·c "REJECTED"
    reason: str
    voted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class EvolutionTransaction(BaseModel):
    """Giao dá»‹ch tiáº¿n hÃ³a Ä‘Ã£ Ä‘Æ°á»£c phÃª duyá»‡t vÃ  ghi sá»•."""

    tx_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    evolution_id: str
    votes: list[CouncilVote]
    status: str  # "APPROVED" hoáº·c "REJECTED"


class EvolutionGovernanceCouncil:
    """Há»™i Ä‘á»“ng giÃ¡m sÃ¡t biá»ƒu quyáº¿t cho cÃ¡c Ä‘á» xuáº¥t tá»± tiáº¿n hÃ³a."""

    def __init__(self, ledger_path: str = "runtime/traces/evolution_ledger.jsonl") -> None:
        self.ledger_path = ledger_path
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)

    def evaluate_proposal(self, obj: EvolutionObject, votes: list[CouncilVote]) -> EvolutionTransaction:
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
