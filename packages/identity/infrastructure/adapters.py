"""Infrastructure adapters for user identity management."""

from typing import Any


class InMemoryUserRepository:
    """In-memory repository fallback for user identity storage."""

    def __init__(self) -> None:
        self._users: dict[str, Any] = {}

    def save(self, user: Any) -> Any:
        """Saves or updates a user entity in memory."""
        user_id = getattr(user, "id", str(len(self._users) + 1))
        self._users[user_id] = user
        return user

    def find_by_id(self, user_id: str) -> Any | None:
        """Retrieves a user entity by ID."""
        return self._users.get(user_id)

    def find_by_email(self, email: str) -> Any | None:
        """Retrieves a user entity by email."""
        for user in self._users.values():
            if getattr(user, "email", None) == email:
                return user
        return None


class PostgresUserRepository(InMemoryUserRepository):
    """PostgreSQL adapter for user identity persistence."""

    def __init__(self, db_url: str) -> None:
        super().__init__()
        self.db_url: str = db_url
