"""Message Queue and Event Mesh adapter for asynchronous messaging."""

from typing import Any


class MessageQueueAdapter:
    """Adapter for broadcasting domain events across message brokers."""

    def __init__(self) -> None:
        self._messages: list[dict[str, Any]] = []

    def publish_message(
        self,
        topic: str,
        payload: dict[str, Any],
    ) -> bool:
        """Publishes message event to target topic channel."""
        self._messages.append({"topic": topic, "payload": payload})
        return True
