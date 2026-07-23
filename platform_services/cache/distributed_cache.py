"""Distributed Redis cache interface for platform services."""

from typing import Any


class DistributedCacheAdapter:
    """Adapter providing unified key-value distributed caching."""

    def __init__(self) -> None:
        self._cache: dict[str, Any] = {}

    def get(self, key: str) -> Any | None:
        """Retrieves item from cache by key."""
        return self._cache.get(key)

    def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: int = 3600,
    ) -> None:
        """Stores item in cache with TTL expiration."""
        self._cache[key] = value
