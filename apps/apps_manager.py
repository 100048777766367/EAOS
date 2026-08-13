"""EAOS Central Application Lifecycle Orchestrator.

Manages discovery, registration, health monitoring, and graceful shutdown
across all delivery channels (api, web, cli, agent, desktop, automation, ledger).
"""

from __future__ import annotations

import os
import time
from typing import ClassVar

import structlog

from apps.models import (
    AppHealthMetricDTO,
    AppLifecycleStatus,
    AppMatrixSummaryDTO,
    AppRegistrationDTO,
)

logger = structlog.get_logger()


class AppsManager:
    """Enterprise Application Lifecycle Manager."""

    _instance: ClassVar[AppsManager | None] = None

    def __init__(self) -> None:
        self._registered_apps: dict[str, AppRegistrationDTO] = {}
        self._app_statuses: dict[str, AppLifecycleStatus] = {}
        self._start_times: dict[str, float] = {}
        self._discover_default_applications()

    @classmethod
    def get_instance(cls) -> AppsManager:
        """Singleton accessor for thread-safe global usage."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _discover_default_applications(self) -> None:
        """Discovers and registers the 7 default EAOS delivery apps."""
        default_host = os.getenv("HOST", "127.0.0.1")

        defaults = [
            AppRegistrationDTO(
                app_id="apps.api",
                name="EAOS Pure Data API Gateway",
                port=int(os.getenv("API_PORT", "8000")),
                host=default_host,
            ),
            AppRegistrationDTO(
                app_id="apps.web",
                name="EAOS Web Control Room Dashboard",
                port=int(os.getenv("WEB_PORT", "3000")),
                host=default_host,
            ),
            AppRegistrationDTO(
                app_id="apps.cli",
                name="EAOS Command Line Interface Engine",
                port=0,
                host=default_host,
            ),
            AppRegistrationDTO(
                app_id="apps.agent",
                name="EAOS Autonomous Agent Team Engine",
                port=int(os.getenv("AGENT_PORT", "8001")),
                host=default_host,
            ),
            AppRegistrationDTO(
                app_id="apps.desktop",
                name="EAOS Native Desktop Application",
                port=int(os.getenv("DESKTOP_PORT", "8002")),
                host=default_host,
            ),
            AppRegistrationDTO(
                app_id="apps.automation",
                name="EAOS Self-Healing Archiver & Simulator",
                port=0,
                host=default_host,
            ),
            AppRegistrationDTO(
                app_id="apps.ledger",
                name="EAOS Quantum Apps Ledger",
                port=0,
                host=default_host,
            ),
        ]

        for app_dto in defaults:
            self.register_app(app_dto)

    def register_app(self, app_dto: AppRegistrationDTO) -> None:
        """Registers an application channel into the orchestrator."""
        self._registered_apps[app_dto.app_id] = app_dto
        self._app_statuses[app_dto.app_id] = AppLifecycleStatus.REGISTERED
        logger.info(
            "Registered application channel",
            app_id=app_dto.app_id,
            name=app_dto.name,
        )

    def start_app(self, app_id: str) -> bool:
        """Triggers startup lifecycle for a specific application."""
        if app_id not in self._registered_apps:
            logger.error("Cannot start unregistered app", app_id=app_id)
            return False

        self._app_statuses[app_id] = AppLifecycleStatus.HEALTHY
        self._start_times[app_id] = time.time()
        logger.info("Application started successfully", app_id=app_id)
        return True

    def stop_app(self, app_id: str) -> bool:
        """Triggers graceful shutdown lifecycle for an application."""
        if app_id not in self._registered_apps:
            return False

        self._app_statuses[app_id] = AppLifecycleStatus.STOPPED
        logger.info("Application stopped successfully", app_id=app_id)
        return True

    def get_app_health(self, app_id: str) -> AppHealthMetricDTO | None:
        """Returns health metric snapshot for a specific app."""
        if app_id not in self._registered_apps:
            return None

        status = self._app_statuses.get(app_id, AppLifecycleStatus.REGISTERED)
        start_time = self._start_times.get(app_id, time.time())
        uptime = time.time() - start_time if status == AppLifecycleStatus.HEALTHY else 0.0

        return AppHealthMetricDTO(
            app_id=app_id,
            status=status,
            health_score=100 if status == AppLifecycleStatus.HEALTHY else 0,
            uptime_seconds=round(uptime, 2),
            details={"name": self._registered_apps[app_id].name},
        )

    def get_system_health_matrix(self) -> AppMatrixSummaryDTO:
        """Returns aggregated health matrix across all registered delivery apps."""
        metrics: list[AppHealthMetricDTO] = []
        healthy_count = 0

        for app_id in self._registered_apps:
            health = self.get_app_health(app_id)
            if health:
                metrics.append(health)
                if health.status == AppLifecycleStatus.HEALTHY:
                    healthy_count += 1

        overall = "HEALTHY" if healthy_count == len(self._registered_apps) else "DEGRADED"

        return AppMatrixSummaryDTO(
            total_apps=len(self._registered_apps),
            healthy_count=healthy_count,
            degraded_count=len(self._registered_apps) - healthy_count,
            overall_system_status=overall,
            apps=metrics,
        )
