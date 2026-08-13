"""Động cơ đăng ký và khám phá dịch vụ."""

from __future__ import annotations

from apps.models import ServiceInstance


class ServiceRegistryEngine:
    """Quản lý Service Discovery và Health Check."""

    def __init__(self) -> None:
        self._services: dict[str, ServiceInstance] = {}

    def register(self, service: ServiceInstance) -> None:
        """Đăng ký dịch vụ mới."""
        self._services[service.service_id] = service

    def get_all_services(self) -> list[ServiceInstance]:
        """Lấy danh sách tất cả dịch vụ."""
        return list(self._services.values())
