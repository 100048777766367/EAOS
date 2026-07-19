from typing import Protocol

from packages.civilization.domain.models import (
    AutonomousNegotiation,
    CollectiveEvolutionBlock,
    GlobalConsensusTransaction,
)


class CivilizationRegistryPort(Protocol):
    """Port định nghĩa các hành vi mật mã và đàm phán văn minh."""

    def save_negotiation(
        self, neg: AutonomousNegotiation
    ) -> AutonomousNegotiation: ...

    def find_negotiation_by_id(
        self, proposal_id: str
    ) -> AutonomousNegotiation | None: ...

    def save_evolution_block(
        self, block: CollectiveEvolutionBlock
    ) -> CollectiveEvolutionBlock: ...

    def get_latest_block(self) -> CollectiveEvolutionBlock: ...

    def list_evolution_blocks(self) -> list[CollectiveEvolutionBlock]: ...

    def save_consensus_transaction(
        self, tx: GlobalConsensusTransaction
    ) -> GlobalConsensusTransaction: ...

    def find_consensus_by_id(
        self, tx_id: str
    ) -> GlobalConsensusTransaction | None: ...