import hashlib
import uuid
from datetime import UTC, datetime

from pydantic import BaseModel

from packages.civilization.domain.models import (
    AutonomousNegotiation,
    CollectiveEvolutionBlock,
    GlobalConsensusTransaction,
)
from packages.civilization.domain.ports import CivilizationRegistryPort


class NegotiationRequest(BaseModel):
    offering_member_id: str
    demanding_member_id: str
    capability_exchanged: str
    cost_tokens: float


class ConsensusRequest(BaseModel):
    proposal_id: str
    approvals_count: int
    total_participants: int


class ExecuteCivilizationCivilianUseCase:
    """Application Service điều phối đàm phán và đúc sổ cái liên bang vĩnh cửu."""

    def __init__(self, repo: CivilizationRegistryPort) -> None:
        self.repo = repo

    def negotiate_capability_exchange(self, request: NegotiationRequest) -> AutonomousNegotiation:
        neg_id = f"NEG-{uuid.uuid4().hex[:6].upper()}"
        neg = AutonomousNegotiation(
            id=neg_id,
            offering_member_id=request.offering_member_id,
            demanding_member_id=request.demanding_member_id,
            capability_id=request.capability_exchanged,
            capability_exchanged=request.capability_exchanged,
            initial_offer_tokens=request.cost_tokens,
            counter_offer_tokens=request.cost_tokens,
            cost_tokens=request.cost_tokens,
            status="SETTLED",
            created_at=datetime.now(UTC),
        )
        return self.repo.save_negotiation(neg)

    def commit_global_consensus(self, request: ConsensusRequest) -> GlobalConsensusTransaction:
        proposal = self.repo.find_negotiation_by_id(request.proposal_id)
        if not proposal:
            raise ValueError(f"Không tìm thấy đề xuất: {request.proposal_id}")

        if request.approvals_count < (request.total_participants / 2):
            raise ValueError("Đồng thuận không đạt thế đa số.")

        tx_id = f"TX-CIV-{uuid.uuid4().hex[:8].upper()}"
        tx = GlobalConsensusTransaction(
            tx_id=tx_id,
            proposal_id=request.proposal_id,
            status="COMMITTED",
            committed_at=datetime.now(UTC),
        )

        latest_block = self.repo.get_latest_block()
        prev_hash = latest_block.hash if latest_block else "GENESIS_HASH"
        prev_index = latest_block.index if latest_block else 0

        block_hash = hashlib.sha256(f"{prev_index + 1}{prev_hash}{proposal.id}".encode()).hexdigest()

        new_block = CollectiveEvolutionBlock(
            index=prev_index + 1,
            previous_hash=prev_hash,
            hash=block_hash,
            payload_summary=f"Consensus committed for {proposal.id}",
            timestamp=datetime.now(UTC),
        )
        self.repo.save_block(new_block)

        return self.repo.save_consensus_transaction(tx)
