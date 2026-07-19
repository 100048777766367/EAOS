import uuid
from datetime import UTC, datetime, timedelta

from pydantic import BaseModel

from packages.civilization.domain.models import (
    AutonomousNegotiation,
    CollectiveEvolutionBlock,
    FederatedCouncilVote,
    GlobalConsensusTransaction,
    calculate_block_hash,
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
    """Application Service quản lý các thỏa ước và tiến hóa nền văn minh."""

    def __init__(self, registry: CivilizationRegistryPort) -> None:
        self.registry = registry

    def negotiate_capability_exchange(
        self, request: NegotiationRequest
    ) -> AutonomousNegotiation:
        neg_id = f"NEG-{uuid.uuid4().hex[:6].upper()}"

        # BƯỚC 1: OFFER (Phát lệnh đề xuất giá thô từ bên yêu cầu)
        initial_offer = request.cost_tokens

        # BƯỚC 2: COUNTER OFFER (Bên cung cấp phân tích và điều chỉnh biểu giá)
        # Giả lập tăng 10% phí dịch vụ theo biểu phí hạ tầng
        counter_offer = round(initial_offer * 1.1, 2)

        # BƯỚC 3: POLICY CHECK (Cả hai bên tự chẩn đoán chính sách nội bộ)
        policy_passed = counter_offer > 0

        if not policy_passed:
            neg = AutonomousNegotiation(
                id=neg_id,
                offering_member_id=request.offering_member_id,
                demanding_member_id=request.demanding_member_id,
                capability_id=request.capability_exchanged,
                initial_offer_tokens=initial_offer,
                counter_offer_tokens=counter_offer,
                status="REJECTED",
            )
            return self.registry.save_negotiation(neg)

        # BƯỚC 4: AGREEMENT (Đạt thỏa ước thành công)
        # BƯỚC 5: SETTLEMENT (Khấu trừ hoàn tất giao dịch tự trị)
        settlement_tx_id = f"SETTLE-TX-{uuid.uuid4().hex[:8].upper()}"

        neg = AutonomousNegotiation(
            id=neg_id,
            offering_member_id=request.offering_member_id,
            demanding_member_id=request.demanding_member_id,
            capability_id=request.capability_exchanged,
            initial_offer_tokens=initial_offer,
            counter_offer_tokens=counter_offer,
            status="SETTLED",
            settlement_tx_id=settlement_tx_id,
        )
        return self.registry.save_negotiation(neg)

    def commit_global_consensus(
        self, request: ConsensusRequest
    ) -> GlobalConsensusTransaction:
        tx_id = f"TX-CIV-{uuid.uuid4().hex[:8].upper()}"

        # BƯỚC 1: PROPOSAL (Tạo đề xuất mới)
        # BƯỚC 2: BROADCAST (Truyền phát thông điệp chéo tổ chức qua Event Mesh)
        topic = "governance.ontology.broadcast"

        # BƯỚC 3: COLLECT VOTES (Thu thập phi đồng bộ phiếu biểu quyết)
        votes = [
            FederatedCouncilVote(
                voter_member_id="Enterprise-A",
                voter_agent_role="ArchitectAgent",
                decision="APPROVED",
                reason="Ecosystem compatibility verified.",
            )
        ]

        # BƯỚC 4: TIMEOUT (Kiểm tra xem có vượt quá giới hạn thời gian họp hay không)
        # Giả lập thời gian giới hạn họp là 1 giờ sau
        timeout_at = datetime.now(UTC) + timedelta(hours=1)

        # BƯỚC 5: COMMIT (Ký sổ đúc khối vĩnh cửu nếu đạt đa số phiếu thuận)
        passed = request.approvals_count >= (request.total_participants / 2)
        status = "COMMITTED" if passed else "FAILED"

        tx = GlobalConsensusTransaction(
            tx_id=tx_id,
            proposal_id=request.proposal_id,
            broadcast_topic=topic,
            votes=votes,
            timeout_at=timeout_at,
            status=status,
        )
        self.registry.save_consensus_transaction(tx)

        if status == "COMMITTED":
            # TRUY VẾT LIÊN KẾT MẬT MÃ (Genesis -> Block1 -> Block2)
            latest_block = self.registry.get_latest_block()
            new_index = latest_block.index + 1
            prev_hash = latest_block.current_hash

            timestamp = datetime.now(UTC)
            payload = {
                "tx_id": tx_id,
                "proposal_id": request.proposal_id,
                "consensus_status": "PASSED",
            }

            # Tính toán Hash chuỗi đệ quy
            curr_hash = calculate_block_hash(new_index, prev_hash, timestamp, payload)

            block = CollectiveEvolutionBlock(
                index=new_index,
                previous_hash=prev_hash,
                current_hash=curr_hash,
                timestamp=timestamp,
                payload=payload,
                signature=f"SIG-FED-{uuid.uuid4().hex[:8].upper()}",
            )
            self.registry.save_evolution_block(block)

        return tx
