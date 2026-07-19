from datetime import UTC, datetime

from packages.civilization.domain.models import (
    AutonomousNegotiation,
    CollectiveEvolutionBlock,
    GlobalConsensusTransaction,
    calculate_block_hash,
)
from packages.civilization.domain.ports import CivilizationRegistryPort


class InMemoryCivilizationRegistry(CivilizationRegistryPort):
    """Adapter bộ nhớ RAM lưu trữ sổ cái có đo đạc chiều cao Block Height."""

    def __init__(self) -> None:
        self._negotiations: dict[str, AutonomousNegotiation] = {}
        self._blocks: list[CollectiveEvolutionBlock] = []
        self._txs: dict[str, GlobalConsensusTransaction] = {}
        self._idempotency_keys: set[str] = set()

        # Khởi tạo khối Genesis
        genesis_payload = {"system_message": "EAOS Genesis Block Initialized."}
        genesis_timestamp = datetime(2026, 1, 1, tzinfo=UTC)
        genesis_prev_hash = "0" * 64

        genesis_hash = calculate_block_hash(
            index=0,
            previous_hash=genesis_prev_hash,
            timestamp=genesis_timestamp,
            payload=genesis_payload,
        )

        genesis_block = CollectiveEvolutionBlock(
            index=0,
            previous_hash=genesis_prev_hash,
            current_hash=genesis_hash,
            timestamp=genesis_timestamp,
            payload=genesis_payload,
            signature="SIG-GENESIS-ROOT",
        )
        self.save_evolution_block(genesis_block)

    def save_negotiation(self, neg: AutonomousNegotiation) -> AutonomousNegotiation:
        self._negotiations[neg.id] = neg
        return neg

    def find_negotiation_by_id(self, proposal_id: str) -> AutonomousNegotiation | None:
        return self._negotiations.get(proposal_id)

    def save_evolution_block(
        self, block: CollectiveEvolutionBlock
    ) -> CollectiveEvolutionBlock:
        self._blocks.append(block)
        return block

    def get_latest_block(self) -> CollectiveEvolutionBlock:
        return self._blocks[-1]

    def list_evolution_blocks(self) -> list[CollectiveEvolutionBlock]:
        return self._blocks

    def save_consensus_transaction(
        self, tx: GlobalConsensusTransaction
    ) -> GlobalConsensusTransaction:
        self._txs[tx.tx_id] = tx
        return tx

    def find_consensus_by_id(self, tx_id: str) -> GlobalConsensusTransaction | None:
        return self._txs.get(tx_id)

    def get_block_height(self) -> int:
        """Đo đạc chỉ số (Metrics): Chiều cao của sổ cái chuỗi khối."""
        # Chỉ số chiều cao = tổng số khối trừ đi khối Genesis
        return max(0, len(self._blocks) - 1)
