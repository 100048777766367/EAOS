from typing import Protocol

from packages.learning.domain.models import Experience


class ExperienceRepository(Protocol):
    """Port định nghĩa các hành vi lưu trữ tri thức kinh nghiệm."""

    def save(self, exp: Experience) -> Experience: ...

    def find_by_id(self, exp_id: str) -> Experience | None: ...

    def list_all(self) -> list[Experience]: ...