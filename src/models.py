"""Mô hình DTO cho hệ thống Mã nguồn Cốt lõi (SRC)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceDomainSnapshot:
    """Ảnh chụp trạng thái phân lớp Clean Architecture.

    Attributes:
        total_aggregates: Số lượng aggregate trong miền.
        total_use_cases: Số lượng use case đã phát hiện.
        is_pure_domain: True nếu chỉ chứa logic domain thuần.
        quantum_proof: Chuỗi mô tả bằng chứng lượng tử/metadata liên quan.
    """

    total_aggregates: int
    total_use_cases: int
    is_pure_domain: bool
    quantum_proof: str
