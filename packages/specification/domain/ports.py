from typing import Protocol

from packages.specification.domain.models import EnterpriseSpecification


class SpecificationRegistryPort(Protocol):
    """Port định nghĩa hành vi quản lý và đăng ký đặc tả doanh nghiệp."""

    def register(self, spec: EnterpriseSpecification) -> EnterpriseSpecification: ...

    def find_by_id(self, spec_id: str) -> EnterpriseSpecification | None: ...

    def list_all(self) -> list[EnterpriseSpecification]: ...
