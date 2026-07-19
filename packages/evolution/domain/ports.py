from typing import Protocol

from packages.evolution.domain.models import EvolutionObject, RollbackSnapshot


class EvolutionRepository(Protocol):
    """Port định nghĩa hành vi lưu trữ, rollback và truy vết gia phả."""

    def save(self, obj: EvolutionObject) -> EvolutionObject: ...

    def find_by_id(self, obj_id: str) -> EvolutionObject | None: ...

    def get_lineage(self, start_id: str) -> list[str]: ...

    def save_snapshot(self, snapshot: RollbackSnapshot) -> RollbackSnapshot: ...

    def find_snapshot(self, snapshot_id: str) -> RollbackSnapshot | None: ...
