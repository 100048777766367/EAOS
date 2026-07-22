from datetime import UTC, datetime

from packages.civilization.domain.models import (
    AutonomousNegotiation,
    CollectiveEvolutionBlock,
    GlobalConsensusTransaction,
    calculate_block_hash,
)
from packages.civilization.domain.ports import CivilizationRegistryPort


class InMemoryCivilizationRegistry(CivilizationRegistryPort):
    def __init__(self) -> None:
        self._negotiations: dict[str, AutonomousNegotiation] = {}
        self._transactions: dict[str, GlobalConsensusTransaction] = {}
        self._blocks: list[CollectiveEvolutionBlock] = []

        now_dt = datetime.now(UTC)
        genesis_hash = calculate_block_hash(
            index=0,
            previous_hash="0" * 64,
            payload_summary="Genesis Evolution Block",
            timestamp=now_dt,
        )
        genesis_block = CollectiveEvolutionBlock(
            index=0,
            previous_hash="0" * 64,
            hash=genesis_hash,
            current_hash=genesis_hash,
            payload_summary="Genesis Evolution Block",
            timestamp=now_dt,
        )
        self._blocks.append(genesis_block)

    def save_negotiation(
        self, neg: AutonomousNegotiation
    ) -> AutonomousNegotiation:
        self._negotiations[neg.id] = neg
        return neg

    def find_negotiation_by_id(
        self, neg_id: str
    ) -> AutonomousNegotiation | None:
        return self._negotiations.get(neg_id)

    def save_consensus_transaction(
        self, tx: GlobalConsensusTransaction
    ) -> GlobalConsensusTransaction:
        self._transactions[tx.tx_id] = tx
        return tx

    def save_block(
        self, block: CollectiveEvolutionBlock
    ) -> CollectiveEvolutionBlock:
        self._blocks.append(block)
        return block

    def get_latest_block(self) -> CollectiveEvolutionBlock | None:
        return self._blocks[-1] if self._blocks else None

    def list_evolution_blocks(self) -> list[CollectiveEvolutionBlock]:
        return self._blocks
