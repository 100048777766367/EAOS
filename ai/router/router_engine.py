from __future__ import annotations

"""Động cơ tính toán chi phí điều tuyến LLM."""


class RouterEngine:
    """Tính toán SLA và chi phí token."""

    def estimate_cost(self, prompt_tokens: int) -> float:
        """Ước tính chi phí cuộc gọi."""
        return float(prompt_tokens * 0.00001)
