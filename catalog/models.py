from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

"""Mô hình DTO cho hệ thống Danh mục Phần tử Domain (CATALOG)."""


class CatalogElementType(StrEnum):
    """Phân loại Phần tử Domain CQRS/DDD."""

    AGGREGATE = "AGGREGATE"
    ENTITY = "ENTITY"
    COMMAND = "COMMAND"
    QUERY = "QUERY"
    EVENT = "EVENT"


@dataclass(frozen=True)
class DomainElementRecord:
    """Bản ghi Phần tử Domain."""

    element_id: str
    name: str
    element_type: CatalogElementType
    bounded_context: str


@dataclass
class CatalogQueryResult:
    """Kết quả truy vấn Danh mục Phần tử Domain."""

    total_elements: int
    elements: list[DomainElementRecord] = field(default_factory=list)
    proof_hash: str = ""
