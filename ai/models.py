from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

"""Mô hình DTO cho hệ thống Trí tuệ Nhân tạo Doanh nghiệp (AI)."""


class ModelTier(StrEnum):
    """Phân cấp Mô hình ai."""

    FAST = "FAST"
    BALANCED = "BALANCED"
    HIGH_REASONING = "HIGH_REASONING"


@dataclass(frozen=True)
class InferenceRequest:
    """Thẻ yêu cầu Suy luận ai."""

    prompt: str
    tier: ModelTier = ModelTier.BALANCED
    max_tokens: int = 2048
    temperature: float = 0.2


@dataclass
class InferenceResult:
    """Kết quả Suy luận ai."""

    text: str
    provider: str
    prompt_tokens: int
    completion_tokens: int
    proof_hash: str = ""
