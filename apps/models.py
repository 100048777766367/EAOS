from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

"""EAOS Application Models and Lifecycle Data Transfer Objects.

Provides Pydantic v2 schemas for application registration, health matrix,
telemetry tracking, and status monitoring.
"""


class AppLifecycleStatus(StrEnum):
    """Lifecycle execution state of an EAOS application."""

    REGISTERED = "REGISTERED"
    STARTING = "STARTING"
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"


class AppRegistrationDTO(BaseModel):
    """Data transfer object for registering a new application channel."""

    model_config = ConfigDict(frozen=True)

    app_id: str = Field(description="Unique identifier for the app")
    name: str = Field(description="Human readable application name")
    version: str = Field(default="0.1.0")
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8000)
    enabled: bool = Field(default=True)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AppHealthMetricDTO(BaseModel):
    """Health and telemetry status snapshot for an application."""

    model_config = ConfigDict(frozen=True)

    app_id: str
    status: AppLifecycleStatus
    health_score: int = Field(ge=0, le=100, default=100)
    uptime_seconds: float = Field(default=0.0)
    last_check_time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    details: dict[str, Any] = Field(default_factory=dict)


class AppMatrixSummaryDTO(BaseModel):
    """Aggregated health summary matrix across all delivery applications."""

    model_config = ConfigDict(frozen=True)

    total_apps: int
    healthy_count: int
    degraded_count: int
    overall_system_status: str
    apps: list[AppHealthMetricDTO]


class ServiceInstance:
    """Canonical Service Instance DTO."""

    def __init__(self, service_id: str, host: str = "127.0.0.1", port: int = 8000) -> None:
        self.service_id = service_id
        self.host = host
        self.port = port
