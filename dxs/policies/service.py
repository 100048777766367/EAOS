from __future__ import annotations

from dxs.policies.model import Policy


class PolicyService:
    """Application-facing policy registry."""

    def __init__(self) -> None:
        self._policies: dict[str, Policy] = {}

    def register(self, policy: Policy) -> None:
        self._policies[policy.name] = policy

    def get(self, name: str) -> Policy | None:
        return self._policies.get(name)

    def list(self) -> list[Policy]:
        return list(self._policies.values())


__all__ = ["PolicyService"]
