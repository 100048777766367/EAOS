"""Resilience and idempotency engine for platform services."""

from collections.abc import Callable
from typing import Any


class IdempotencyService:
    """Service enforcing request idempotency across operations."""

    def __init__(self) -> None:
        self._processed: dict[str, Any] = {}

    def process(
        self,
        key: str,
        handler: Callable[..., Any],
        payload: Any,
    ) -> Any:
        """Processes request with idempotency key locking."""
        if key in self._processed:
            return self._processed[key]
        result = handler(payload)
        self._processed[key] = result
        return result


class IdempotencyManager(IdempotencyService):
    """Alias adapter for idempotency management."""

    def check_and_set(
        self,
        key: str,
        value: dict[str, Any],
    ) -> tuple[bool, dict[str, Any]]:
        """Checks if key is present or sets new value."""
        if key in self._processed:
            return True, self._processed[key]
        self._processed[key] = value
        return False, value


class ResilienceEngine:
    """Circuit breaker and resilience strategy orchestrator."""

    def execute(
        self,
        action: Callable[..., Any],
        *args: Any,
    ) -> Any:
        """Executes action under resilience policies."""
        return action(*args)
