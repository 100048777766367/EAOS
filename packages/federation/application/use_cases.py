import uuid
from datetime import UTC, datetime

from tools.digital_twin.digital_twin import DigitalTwinOrchestrator

from packages.federation.domain.models import (
    CollectiveEvolutionReport,
    EcosystemMember,
    FederatedCouncilVote,
    FederatedTransaction,
    SharedKnowledgePacket,
)
from packages.federation.domain.ports import FederationRepositoryPort


class CollectiveEvolutionUseCase:
    """Application Service điều phối việc tiếp nhận và giả lập học hỏi tập thể."""

    def __init__(
        self,
        registry: FederationRepositoryPort,
        digital_twin: DigitalTwinOrchestrator,
    ) -> None:
        self.registry = registry
        self.digital_twin = digital_twin

    def process_shared_knowledge(
        self, receiver_id: str, packet: SharedKnowledgePacket
    ) -> CollectiveEvolutionReport:
        member = self.registry.find_member_by_id(receiver_id)
        if not member:
            raise ValueError(f"Không tìm thấy thành viên: {receiver_id}")

        simulated_proposal = {
            "package_name": f"evolved-{packet.heuristic_id.lower()}",
            "layer": "infrastructure",
            "dependencies": ["packages.knowledge.domain"],
        }

        twin_result = self.digital_twin.evaluate_proposal(simulated_proposal)
        simulated_score = twin_result["current_score"]

        if twin_result["status"] == "APPROVED":
            status = "ADOPTED"
            reason = (
                f"Học hỏi thành công từ {packet.sender_id}. "
                "Cấu hình tương thích 100% với hiến pháp cục bộ."
            )
        else:
            status = "REJECTED"
            reason = (
                f"Từ chối tiếp nhận chính sách từ {packet.sender_id}. "
                "Vi phạm ranh giới hiến pháp cục bộ."
            )

        report = CollectiveEvolutionReport(
            member_id=receiver_id,
            received_from_id=packet.sender_id,
            status=status,
            reason=reason,
            simulated_score=simulated_score,
        )

        return self.registry.save_evolution_report(report)


class ExecuteFederatedGovernanceUseCase:
    """Application Service điều phối biểu quyết liên minh đa tổ chức."""

    def __init__(self, registry: FederationRepositoryPort) -> None:
        self.registry = registry

    def vote_on_shared_ontology(
        self, target_ontology_id: str, votes: list[FederatedCouncilVote]
    ) -> FederatedTransaction:
        approved_voters = [v for v in votes if v.decision == "APPROVED"]
        passed = len(approved_voters) >= (len(votes) / 2)

        tx_id = f"TX-FED-{uuid.uuid4().hex[:8].upper()}"
        status = "APPROVED" if passed else "REJECTED"

        tx = FederatedTransaction(
            tx_id=tx_id,
            target_ontology_id=target_ontology_id,
            votes=votes,
            status=status,
            timestamp=datetime.now(UTC),
        )

        return self.registry.save_federated_transaction(tx)


class HeartbeatUseCase:
    """Application Service chịu trách nhiệm ghi nhận Heartbeat và kiểm tra Health."""

    def __init__(self, registry: FederationRepositoryPort) -> None:
        self.registry = registry

    def execute_heartbeat(self, member_id: str) -> EcosystemMember:
        member = self.registry.find_member_by_id(member_id)
        if not member:
            raise ValueError(f"Không tìm thấy thành viên: {member_id}")

        # Tự chẩn đoán Health status dựa trên Capability Index
        simulated_health = "HEALTHY"
        if len(member.capabilities_index) == 0:
            simulated_health = "DEGRADED"

        updated = member.model_copy(
            update={
                "last_heartbeat": datetime.now(UTC),
                "health_status": simulated_health,
            }
        )
        return self.registry.register_member(updated)
