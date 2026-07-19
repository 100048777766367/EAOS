from typing import Protocol

from packages.autonomous.domain.models import LoopCycle


class AutonomousRepository(Protocol):
    """Port định nghĩa các hành vi lưu trữ và chẩn đoán vòng lặp tự trị."""

    def save(self, cycle: LoopCycle) -> LoopCycle: ...

    def find_by_id(self, cycle_id: str) -> LoopCycle | None: ...

    def list_all(self) -> list[LoopCycle]: ...
