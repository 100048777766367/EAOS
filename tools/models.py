from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

"""Mô hình DTO cho hệ thống Công cụ và Tiện ích Kiến trúc (TOOLS)."""


class ToolCategory(StrEnum):
    """Phân loại Công cụ."""

    CLI = "CLI"
    DOCTOR = "DOCTOR"
    AUDIT = "AUDIT"
    CHAOS = "CHAOS"
    FITNESS = "FITNESS"
    VALIDATE = "VALIDATE"


@dataclass(frozen=True)
class ToolExecutionResult:
    """Kết quả thực thi công cụ."""

    tool_name: str
    success: bool
    output: str
    proof_hash: str = ""


@dataclass
class DoctorCheckSummary:
    """Tóm tắt chẩn đoán sức khỏe Doctor v2."""

    score: int
    total_checkers: int
    failed_checkers: list[str] = field(default_factory=list)
