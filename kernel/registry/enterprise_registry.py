from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RegistryResource(BaseModel):
    """Đối tượng tài nguyên được đăng ký trong hệ điều hành doanh nghiệp."""

    id: str = Field(..., description="Mã tài nguyên duy nhất")
    type: str = Field(
        ...,
        description="Phân loại: CAPABILITY, SPECIFICATION, WORKFLOW, AGENT...",
    )
    name: str = Field(..., description="Tên tài nguyên hiển thị")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Siêu dữ liệu chi tiết đi kèm"
    )

    model_config = ConfigDict(frozen=True)


class EnterpriseRegistry:
    """Hệ thống Service Discovery trung tâm để tự động khám phá tài nguyên."""

    def __init__(self) -> None:
        self._resources: dict[str, RegistryResource] = {}

    def register(self, resource: RegistryResource) -> RegistryResource:
        """Đăng ký một tài nguyên mới vào hệ thống Discovery."""
        self._resources[resource.id] = resource
        return resource

    def find_by_id(self, resource_id: str) -> RegistryResource | None:
        """Tìm kiếm một tài nguyên cụ thể theo mã ID."""
        return self._resources.get(resource_id)

    def list_by_type(self, resource_type: str) -> list[RegistryResource]:
        """Liệt kê toàn bộ tài nguyên theo phân loại."""
        return [
            r
            for r in self._resources.values()
            if r.type.upper() == resource_type.upper()
        ]

    def list_all(self) -> list[RegistryResource]:
        """Liệt kê toàn bộ tài nguyên trong hệ thống."""
        return list(self._resources.values())
