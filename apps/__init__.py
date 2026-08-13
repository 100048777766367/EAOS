"""EAOS Delivery Applications Master Package.

Provides centralized management for API, Web, CLI, Agent, Desktop, Automation,
and Ledger delivery channels.
"""

from apps.apps_manager import AppsManager
from apps.models import (
    AppHealthMetricDTO,
    AppLifecycleStatus,
    AppMatrixSummaryDTO,
    AppRegistrationDTO,
)

__all__ = [
    "AppHealthMetricDTO",
    "AppLifecycleStatus",
    "AppMatrixSummaryDTO",
    "AppRegistrationDTO",
    "AppsManager",
]
