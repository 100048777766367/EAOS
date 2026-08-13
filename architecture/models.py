from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

"""Mô hình DTO cho hệ thống Kiến trúc Doanh nghiệp (ARCHITECTURE)."""


class C4Level(StrEnum):
    """Cấp độ mô hình C4."""

    CONTEXT = "CONTEXT"
    CONTAINER = "CONTAINER"
    COMPONENT = "COMPONENT"
    CODE = "CODE"


@dataclass(frozen=True)
class CanonicalLayerRecord:
    """Thẻ lưu trữ thông tin Tầng Kiến trúc chuẩn (52 Layers)."""

    layer_number: int
    name: str
    domain_boundary: str


@dataclass
class ArchitectureSnapshot:
    """Ảnh chụp trạng thái Kiến trúc Doanh nghiệp."""

    c4_elements_count: int
    active_adrs_count: int
    canonical_layers_count: int = 52
    proof_hash: str = ""
