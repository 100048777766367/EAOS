from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

"""Mô hình DTO cho hệ thống Trực quan và Tài sản Doanh nghiệp (ASSETS)."""


class AssetType(StrEnum):
    """Phân loại Tài sản Trực quan."""

    DIAGRAM = "DIAGRAM"
    ICON = "ICON"
    LOGO = "LOGO"
    TEMPLATE = "TEMPLATE"


@dataclass(frozen=True)
class VisualAssetRecord:
    """Thẻ lưu trữ thông tin Tài sản Trực quan."""

    asset_id: str
    name: str
    asset_type: AssetType
    file_path: str


@dataclass
class TemplateRenderResult:
    """Kết quả xuất bản Template Markdown."""

    template_id: str
    rendered_markdown: str
    proof_hash: str = ""
