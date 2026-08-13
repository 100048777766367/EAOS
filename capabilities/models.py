from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

"""Mô hình DTO cho hệ thống Năng lực Doanh nghiệp (CAPABILITIES)."""


class CapabilityLevel(StrEnum):
    """Cấp độ Năng lực BIZBOK."""

    STRATEGIC = "STRATEGIC"
    CORE = "CORE"
    SUPPORTING = "SUPPORTING"


@dataclass(frozen=True)
class CapabilityRecord:
    """Bản ghi Năng lực Kinh doanh."""

    capability_id: str
    name: str
    level: CapabilityLevel
    spec_files_count: int = 7


@dataclass
class ContractValidationResult:
    """Kết quả xác thực Hợp đồng Năng lực."""

    capability_id: str
    is_valid: bool
    missing_specs: list[str] = field(default_factory=list)
    proof_hash: str = ""
