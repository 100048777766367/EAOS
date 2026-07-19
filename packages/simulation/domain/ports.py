from typing import Protocol

from packages.simulation.domain.models import Simulation


class SimulationRepository(Protocol):
    """Port định nghĩa các hành vi lưu trữ và truy vấn kết quả mô phỏng."""

    def save(self, sim: Simulation) -> Simulation: ...

    def find_by_id(self, sim_id: str) -> Simulation | None: ...

    def list_all(self) -> list[Simulation]: ...
