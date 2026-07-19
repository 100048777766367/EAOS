from typing import Protocol

from packages.exchange.domain.models import SharedEcosystemEvent


class EcosystemEventMeshPort(Protocol):
    """Port định nghĩa hành vi truyền phát sự kiện xuyên tổ chức (Sprint 4)."""

    def broadcast(self, event: SharedEcosystemEvent) -> SharedEcosystemEvent: ...

    def list_broadcasted_events(self) -> list[SharedEcosystemEvent]: ...
