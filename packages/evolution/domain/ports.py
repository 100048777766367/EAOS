from typing import Protocol

from packages.evolution.domain.models import EvolutionObject


class EvolutionRepository(Protocol):
    """Port định nghĩa các hành vi lưu trữ và truy vết gia phả đối tượng."""

    def save(self, obj: EvolutionObject) -> EvolutionObject: ...

    def find_by_id(self, obj_id: str) -> EvolutionObject | None: ...

    def get_lineage(self, start_id: str) -> list[str]: ...