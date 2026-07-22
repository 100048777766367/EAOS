from typing import Protocol

from packages.autonomous.domain.models import LoopCycle


class AutonomousRepository(Protocol):
    """Port Ä‘á»‹nh nghÄ©a cÃ¡c hÃ nh vi lÆ°u trá»¯ vÃ  cháº©n Ä‘oÃ¡n vÃ²ng láº·p tá»± trá»‹."""

    def save(self, cycle: LoopCycle) -> LoopCycle: ...

    def find_by_id(self, cycle_id: str) -> LoopCycle | None: ...

    def list_all(self) -> list[LoopCycle]: ...
