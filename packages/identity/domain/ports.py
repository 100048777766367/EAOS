from typing import Protocol

from packages.identity.domain.models import User


class UserRepository(Protocol):
    def save(self, user: User) -> User: ...
    def find_by_email(self, email: str) -> User | None: ...
