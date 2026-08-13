"""Organizational Memory for EAOS memory system."""

from typing import Any


class OrganizationalMemory:
    """Manages organizational knowledge and memory structures."""

    def __init__(self) -> None:
        self._storage: list[dict[str, Any]] = []

    def store(self, item: dict[str, Any]) -> None:
        """Store an item into organizational memory."""
        self._storage.append(item)

    def retrieve(self) -> list[dict[str, Any]]:
        """Retrieve organizational memory items."""
        return self._storage
