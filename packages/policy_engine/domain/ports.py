"""Domain ports for Policy Engine context."""

from typing import Any, Protocol

from packages.policy_engine.domain.models import PolicyDocumentAggregate


class PolicyRepositoryPort(Protocol):
    def save(self, policy: PolicyDocumentAggregate) -> None:
        ...

    def find_by_id(self, policy_id: str) -> PolicyDocumentAggregate | None:
        ...

    def list_all(self) -> list[PolicyDocumentAggregate]:
        ...


class ExternalPolicyEnginePort(Protocol):
    """Port for evaluating complex policies via external OPA / Cedar Rego Engine."""

    def evaluate_opa_rego(
        self, policy_path: str, input_context: dict[str, Any]
    ) -> tuple[bool, list[str]]:
        ...
