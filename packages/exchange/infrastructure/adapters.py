from packages.exchange.domain.models import SharedEcosystemEvent
from packages.exchange.domain.ports import EcosystemEventMeshPort


class InMemoryEcosystemEventMesh(EcosystemEventMeshPort):
    """Adapter lÆ°u trá»¯ vÃ  Ä‘iá»u phá»‘i Event Mesh xuyÃªn biÃªn giá»›i doanh nghiá»‡p."""

    def __init__(self) -> None:
        self._events: list[SharedEcosystemEvent] = []

    def broadcast(self, event: SharedEcosystemEvent) -> SharedEcosystemEvent:
        self._events.append(event)
        return event

    def list_broadcasted_events(self) -> list[SharedEcosystemEvent]:
        return self._events

