from typing import Protocol

from packages.learning.domain.models import Experience


class ExperienceRepository(Protocol):
    """Port Ä‘á»‹nh nghÄ©a cÃ¡c hÃ nh vi lÆ°u trá»¯ tri thá»©c kinh nghiá»‡m."""

    def save(self, exp: Experience) -> Experience: ...

    def find_by_id(self, exp_id: str) -> Experience | None: ...

    def list_all(self) -> list[Experience]: ...

