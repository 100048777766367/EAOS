import time
from collections.abc import Callable
from typing import Any


class IdempotencyManager:
    """Manages request idempotency keys to prevent duplicate execution."""

    def __init__(self) -> None:
        self._cache: dict[str, Any] = {}

    def check_and_set(
        self, key: str, payload: Any
    ) -> tuple[bool, Any]:
        if key in self._cache:
            return True, self._cache[key]
        self._cache[key] = payload
        return False, payload


class IdempotencyService:
    """Service wrapper for idempotent function processing."""

    def __init__(self) -> None:
        self._cache: dict[str, Any] = {}

    def process(
        self, key: str, func: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> Any:
        if key in self._cache:
            return self._cache[key]
        result = func(*args, **kwargs)
        self._cache[key] = result
        return result


class ResilienceEngine:
    """Provides automated exponential backoff and retry execution."""

    def __init__(
        self, max_retries: int = 3, backoff_factor: float = 0.1
    ) -> None:
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def execute_with_retry(
        self, func: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> Any:
        last_error: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                time.sleep(self.backoff_factor * (2**attempt))
        raise RuntimeError(
            f"Retry limit ({self.max_retries}) exceeded. Error: {last_error}"
        ) from last_error
