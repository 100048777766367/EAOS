from typing import Protocol

from packages.simulation.domain.models import Simulation


class SimulationRepository(Protocol):
    """Port Ä‘á»‹nh nghÄ©a cÃ¡c hÃ nh vi lÆ°u trá»¯ vÃ  truy váº¥n káº¿t quáº£ mÃ´ phá»ng."""

    def save(self, sim: Simulation) -> Simulation: ...

    def find_by_id(self, sim_id: str) -> Simulation | None: ...

    def list_all(self) -> list[Simulation]: ...

