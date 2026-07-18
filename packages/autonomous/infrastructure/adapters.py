from packages.autonomous.domain.models import LoopCycle
from packages.autonomous.domain.ports import AutonomousRepository


class InMemoryAutonomousRepository(AutonomousRepository):
    """Adapter lưu trữ chu kỳ tiến hóa trong RAM phục vụ kiểm thử."""

    def __init__(self) -> None:
        self._store: dict[str, LoopCycle] = {}

    def save(self, cycle: LoopCycle) -> LoopCycle:
        self._store[cycle.cycle_id] = cycle
        return cycle

    def find_by_id(self, cycle_id: str) -> LoopCycle | None:
        return self._store.get(cycle_id)

    def list_all(self) -> list[LoopCycle]:
        return list(self._store.values())