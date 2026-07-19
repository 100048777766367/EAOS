import asyncio
import inspect
import time
from collections.abc import Callable
from typing import Any, TypeVar

from platform_services.telemetry.observability import TelemetryService

T = TypeVar("T")


class IdempotencyService:
    """Hệ thống chốt chặn Idempotency dùng chung của nền tảng (Platform)."""

    def __init__(self) -> None:
        self._store: dict[str, tuple[float, Any]] = {}

    def process(
        self, key: str, action: Callable[..., T], *args: Any, **kwargs: Any
    ) -> T:
        now = time.time()
        if key in self._store:
            timestamp, cached_res = self._store[key]
            if now - timestamp < 300.0:
                TelemetryService.log_info(
                    "Idempotency match found in Platform", key=key
                )
                return cached_res

        res = action(*args, **kwargs)
        self._store[key] = (now, res)
        return res


class ResilienceEngine:
    """Bộ khung chống lỗi và tự động thử lại (Retry Policy) dùng chung."""

    @staticmethod
    def retry(
        func: Callable[..., Any],
        max_retries: int = 3,
        delay: float = 0.1,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        retries = 0
        last_error: Exception | None = None
        while retries < max_retries:
            try:
                if inspect.iscoroutinefunction(func):
                    return asyncio.run(func(*args, **kwargs))
                return func(*args, **kwargs)
            except Exception as e:
                retries += 1
                last_error = e
                TelemetryService.log_warn(
                    "Transient error, retrying...",
                    func=func.__name__,
                    retry=retries,
                    delay=delay,
                )
                time.sleep(delay)
                delay *= 2.0
        if last_error:
            raise last_error
        raise RuntimeError("Retry policy exhausted")