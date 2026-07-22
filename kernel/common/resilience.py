import asyncio
import inspect
import time
from collections.abc import Callable
from typing import Any

import structlog

logger = structlog.get_logger()


def retry_with_backoff(
    max_retries: int = 3, initial_delay: float = 0.5, backoff_factor: float = 2.0
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator thực hiện Retry có giãn cách exponential backoff."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        if inspect.iscoroutinefunction(func):

            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                delay = initial_delay
                retries = 0
                last_error: Exception | None = None
                while retries < max_retries:
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        retries += 1
                        last_error = e
                        logger.warn(
                            "Transient async error, retrying...",
                            func=func.__name__,
                            retries=retries,
                            delay=delay,
                            error=str(e),
                        )
                        await asyncio.sleep(delay)
                        delay *= backoff_factor
                if last_error:
                    raise last_error
                raise RuntimeError("Retry policy exhausted")

            return async_wrapper

        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            delay = initial_delay
            retries = 0
            last_error: Exception | None = None
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    last_error = e
                    logger.warn(
                        "Transient sync error, retrying...",
                        func=func.__name__,
                        retries=retries,
                        delay=delay,
                        error=str(e),
                    )
                    time.sleep(delay)
                    delay *= backoff_factor
            if last_error:
                raise last_error
            raise RuntimeError("Retry policy exhausted")

        return sync_wrapper

    return decorator


class IdempotencyManager:
    """Bộ kiểm soát Idempotency chống lặp giao dịch (Idempotency Key)."""

    def __init__(self) -> None:
        self._cache: dict[str, tuple[float, Any]] = {}

    def check_and_set(
        self, key: str, payload: Any, ttl_seconds: float = 300.0
    ) -> tuple[bool, Any]:
        """Kiểm tra xem key đã tồn tại chưa. Nếu có, trả về kết quả cũ."""
        now = time.time()
        if key in self._cache:
            timestamp, cached_payload = self._cache[key]
            if now - timestamp < ttl_seconds:
                logger.info("Idempotent request matched", key=key)
                return True, cached_payload

        self._cache[key] = (now, payload)
        return False, payload
