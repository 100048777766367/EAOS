import time
from collections.abc import Callable
from typing import Any

import structlog

logger = structlog.get_logger()


class TelemetryService:
    """Dịch vụ giám sát, đo lường và ghi vết tập trung của Enterprise Platform."""

    @staticmethod
    def log_info(event: str, **kwargs: Any) -> None:
        logger.info(event, **kwargs)

    @staticmethod
    def log_error(event: str, **kwargs: Any) -> None:
        logger.error(event, **kwargs)

    @staticmethod
    def log_warn(event: str, **kwargs: Any) -> None:
        logger.warn(event, **kwargs)

    @staticmethod
    def measure_duration(func: Callable[..., Any]) -> Callable[..., Any]:
        """Tracer ghi vết thời gian thực thi của một tác vụ (Observability)."""

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            try:
                res = func(*args, **kwargs)
                duration = (time.time() - start_time) * 1000.0
                logger.info(
                    "Telemetry Trace",
                    action=func.__name__,
                    status="SUCCESS",
                    duration_ms=round(duration, 2),
                )
                return res
            except Exception as e:
                duration = (time.time() - start_time) * 1000.0
                logger.error(
                    "Telemetry Trace",
                    action=func.__name__,
                    status="FAILED",
                    duration_ms=round(duration, 2),
                    error=str(e),
                )
                raise e

        return wrapper