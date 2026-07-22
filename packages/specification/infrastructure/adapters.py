from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]

from packages.specification.domain.models import (
    EnterpriseSpecification,
    SpecField,
    SpecRule,
)
from packages.specification.domain.ports import SpecificationRegistryPort


class InMemorySpecificationRegistry(SpecificationRegistryPort):
    """Adapter lưu trữ và thông dịch tệp đặc tả YAML trong RAM."""

    def __init__(self) -> None:
        self._store: dict[str, EnterpriseSpecification] = {}

    def register(self, spec: EnterpriseSpecification) -> EnterpriseSpecification:
        self._store[spec.id] = spec
        return spec

    def find_by_id(self, spec_id: str) -> EnterpriseSpecification | None:
        return self._store.get(spec_id)

    def list_all(self) -> list[EnterpriseSpecification]:
        return list(self._store.values())

    def load_from_yaml(self, file_path: Path) -> EnterpriseSpecification:
        if not file_path.exists():
            raise FileNotFoundError(f"Không tìm thấy đặc tả: {file_path}")

        content = file_path.read_text(encoding="utf-8")
        data: dict[str, Any] = yaml.safe_load(content)

        fields = [
            SpecField(
                name=f.get("name", ""),
                type=f.get("type", "str"),
                required=f.get("required", True),
            )
            for f in data.get("fields", [])
        ]

        rules = [
            SpecRule(
                id=r.get("id", "RULE-01"),
                expression=r.get("expression", ""),
                error_message=r.get("error_message", ""),
            )
            for r in data.get("rules", [])
        ]

        return EnterpriseSpecification(
            id=data.get("id", "spec.unknown"),
            name=data.get("name", "Unknown"),
            version=data.get("version", "1.0.0"),
            fields=fields,
            policies=data.get("policies", []),
            rules=rules,
            workflows=data.get("workflows", []),
        )
