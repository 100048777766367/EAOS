from packages.federation.domain.models import (
    CollectiveEvolutionReport,
    EcosystemMember,
    FederatedTransaction,
)
from packages.federation.domain.ports import FederationRepositoryPort


class InMemoryFederationRegistry(FederationRepositoryPort):
    """Adapter bá»™ nhá»› RAM quáº£n lÃ½ káº¿t ná»‘i chÃ©o há»‡ sinh thÃ¡i."""

    def __init__(self) -> None:
        self._members: dict[str, EcosystemMember] = {}
        self._reports: list[CollectiveEvolutionReport] = []
        self._txs: list[FederatedTransaction] = []

    def register_member(self, member: EcosystemMember) -> EcosystemMember:
        self._members[member.id] = member
        return member

    def find_member_by_id(self, member_id: str) -> EcosystemMember | None:
        return self._members.get(member_id)

    def list_members(self) -> list[EcosystemMember]:
        return list(self._members.values())

    def save_evolution_report(self, report: CollectiveEvolutionReport) -> CollectiveEvolutionReport:
        self._reports.append(report)
        return report

    def list_evolution_reports(self) -> list[CollectiveEvolutionReport]:
        return self._reports

    def save_federated_transaction(self, tx: FederatedTransaction) -> FederatedTransaction:
        self._txs.append(tx)
        return tx

    def list_federated_transactions(self) -> list[FederatedTransaction]:
        return self._txs
