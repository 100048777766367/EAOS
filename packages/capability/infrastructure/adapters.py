from pathlib import Path
from typing import Any

import yaml

from packages.capability.domain.models import (
    BusinessCapability,
    CapabilityContract,
    CapabilityMetadata,
)
from packages.capability.domain.ports import CapabilityRegistryPort


class InMemoryCapabilityRegistry(CapabilityRegistryPort):
    """Adapter lưu trữ và giải mã tệp tin cấu hình YAML Năng lực doanh nghiệp."""

    def __init__(self) -> None:
        self._store: dict[str, BusinessCapability] = {}

    def register(self, capability: BusinessCapability) -> BusinessCapability:
        self._store[capability.id] = capability
        return capability

    def find_by_id(self, cap_id: str) -> BusinessCapability | None:
        return self._store.get(cap_id)

    def list_all(self) -> list[BusinessCapability]:
        return list(self._store.values())

    def load_from_yaml(self, file_path: Path) -> BusinessCapability:
        """Đọc quét tệp tin YAML và biên dịch thành mô hình thực thi."""
        if not file_path.exists():
            raise FileNotFoundError(f"Không tìm thấy tệp cấu hình: {file_path}")

        content = file_path.read_text(encoding="utf-8")
        data: dict[str, Any] = yaml.safe_load(content)

        meta_data = CapabilityMetadata(
            owner=data.get("owner", "Architecture Council"),
            status=data.get("status", "active"),
            description=data.get("description", ""),
        )

        contracts = [
            CapabilityContract(
                id=c.get("id", "api"),
                type=c.get("type", "REST"),
                definition_path=c.get("definition_path", ""),
            )
            for c in data.get("contracts", [])
        ]

        return BusinessCapability(
            id=data.get("id", "capability.unknown"),
            name=data.get("name", "Unknown"),
            version=data.get("version", "1.0.0"),
            metadata=meta_data,
            dependencies=data.get("dependencies", []),
            policies=data.get("policies", []),
            contracts=contracts,
            events=data.get("events", []),
        )
