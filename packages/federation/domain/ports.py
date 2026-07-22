from typing import Protocol

from packages.federation.domain.models import (
    CollectiveEvolutionReport,
    EcosystemMember,
    FederatedTransaction,
)


class FederationRepositoryPort(Protocol):
    """Port Ä‘á»‹nh nghÄ©a cÃ¡c hÃ nh vi káº¿t ná»‘i vÃ  khÃ¡m phÃ¡ chÃ©o há»‡ sinh thÃ¡i."""

    def register_member(self, member: EcosystemMember) -> EcosystemMember: ...

    def find_member_by_id(self, member_id: str) -> EcosystemMember | None: ...

    def list_members(self) -> list[EcosystemMember]: ...

    def save_evolution_report(
        self, report: CollectiveEvolutionReport
    ) -> CollectiveEvolutionReport: ...

    def list_evolution_reports(self) -> list[CollectiveEvolutionReport]: ...

    def save_federated_transaction(
        self, tx: FederatedTransaction
    ) -> FederatedTransaction: ...

    def list_federated_transactions(self) -> list[FederatedTransaction]: ...

