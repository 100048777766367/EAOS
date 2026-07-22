from typing import Protocol

from packages.exchange.domain.models import SharedEcosystemEvent


class EcosystemEventMeshPort(Protocol):
    """Port Ä‘á»‹nh nghÄ©a hÃ nh vi truyá»n phÃ¡t sá»± kiá»‡n xuyÃªn tá»• chá»©c (Sprint 4)."""

    def broadcast(self, event: SharedEcosystemEvent) -> SharedEcosystemEvent: ...

    def list_broadcasted_events(self) -> list[SharedEcosystemEvent]: ...

