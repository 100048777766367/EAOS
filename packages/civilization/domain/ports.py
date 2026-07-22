from typing import Protocol

from packages.civilization.domain.models import (
    AutonomousNegotiation,
    CollectiveEvolutionBlock,
    GlobalConsensusTransaction,
)


class CivilizationRegistryPort(Protocol):
    def save_negotiation(self, neg: AutonomousNegotiation) -> AutonomousNegotiation: ...

    def find_negotiation_by_id(self, neg_id: str) -> AutonomousNegotiation | None: ...

    def save_consensus_transaction(self, tx: GlobalConsensusTransaction) -> GlobalConsensusTransaction: ...

    def save_block(self, block: CollectiveEvolutionBlock) -> CollectiveEvolutionBlock: ...

    def get_latest_block(self) -> CollectiveEvolutionBlock | None: ...

    def list_evolution_blocks(self) -> list[CollectiveEvolutionBlock]: ...
