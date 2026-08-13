"""Health model boundary."""

from .model import HealthReport, HealthStatus
from .service import HealthService

__all__ = [
    "HealthReport",
    "HealthService",
    "HealthStatus",
]
