from packages.exchange.domain.models import SharedEcosystemEvent
from packages.exchange.domain.ports import EcosystemEventMeshPort


class InMemoryEcosystemEventMesh(EcosystemEventMeshPort):
    """Adapter lưu trữ và điều phối Event Mesh xuyên biên giới doanh nghiệp."""

    def __init__(self) -> None:
        self._events: list[SharedEcosystemEvent] = []

    def broadcast(self, event: SharedEcosystemEvent) -> SharedEcosystemEvent:
        self._events.append(event)
        return event

    def list_broadcasted_events(self) -> list[SharedEcosystemEvent]:
        return self._events
