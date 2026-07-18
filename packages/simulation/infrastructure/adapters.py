from packages.simulation.domain.models import Simulation
from packages.simulation.domain.ports import SimulationRepository


class InMemorySimulationRepository(SimulationRepository):
    """Adapter lưu trữ kết quả mô phỏng trong RAM phục vụ kiểm thử."""

    def __init__(self) -> None:
        self._store: dict[str, Simulation] = {}

    def save(self, sim: Simulation) -> Simulation:
        self._store[sim.id] = sim
        return sim

    def find_by_id(self, sim_id: str) -> Simulation | None:
        return self._store.get(sim_id)

    def list_all(self) -> list[Simulation]:
        return list(self._store.values())