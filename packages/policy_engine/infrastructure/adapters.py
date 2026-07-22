"""Infrastructure adapters for Policy Engine context."""

import json
import urllib.request
from typing import Any

from packages.policy_engine.domain.models import PolicyDocumentAggregate
from packages.policy_engine.domain.ports import (
    ExternalPolicyEnginePort,
    PolicyRepositoryPort,
)


class InMemoryPolicyRepository(PolicyRepositoryPort):
    def __init__(self) -> None:
        self._store: dict[str, PolicyDocumentAggregate] = {}

    def save(self, policy: PolicyDocumentAggregate) -> None:
        self._store[policy.policy_id] = policy

    def find_by_id(self, policy_id: str) -> PolicyDocumentAggregate | None:
        return self._store.get(policy_id)

    def list_all(self) -> list[PolicyDocumentAggregate]:
        return list(self._store.values())


class OPARegoPolicyAdapter(ExternalPolicyEnginePort):
    """Evaluates Rego policy documents against external Open Policy Agent Daemon via REST API."""

    def __init__(self, opa_host: str = "http://localhost:8181") -> None:
        self.opa_host = opa_host.rstrip("/")

    def evaluate_opa_rego(self, policy_path: str, input_context: dict[str, Any]) -> tuple[bool, list[str]]:
        """Sends POST request to OPA Data API: /v1/data/{policy_path}."""
        url = f"{self.opa_host}/v1/data/{policy_path.strip('/')}"
        headers = {"Content-Type": "application/json"}
        payload = {"input": input_context}

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=3.0) as response:
                if response.status != 200:
                    return False, [f"OPA HTTP Error {response.status}"]

                resp_body = json.loads(response.read().decode("utf-8"))
                result = resp_body.get("result", {})

                allow = bool(result.get("allow", False))
                violations = result.get("violations", [])
                if not isinstance(violations, list):
                    violations = [str(violations)]

                return allow, violations

        except Exception as err:
            # Fallback handling when OPA server is unreachable
            return False, [f"OPA Communication Error: {err}"]
