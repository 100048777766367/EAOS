from packages.learning.domain.models import Experience
from packages.learning.domain.ports import ExperienceRepository


class InMemoryExperienceRepository(ExperienceRepository):
    """Adapter lÆ°u trá»¯ Kinh nghiá»‡m há»c táº­p trong RAM phá»¥c vá»¥ kiá»ƒm thá»­."""

    def __init__(self) -> None:
        self._store: dict[str, Experience] = {}

    def save(self, exp: Experience) -> Experience:
        self._store[exp.id] = exp
        return exp

    def find_by_id(self, exp_id: str) -> Experience | None:
        return self._store.get(exp_id)

    def list_all(self) -> list[Experience]:
        return list(self._store.values())
