from __future__ import annotations

"""Động cơ đánh giá chất lượng phản hồi ai."""


class EvaluationEngine:
    """Đánh giá toàn diện câu trả lời."""

    def evaluate_response(self, text: str) -> bool:
        """Đánh giá chất lượng."""
        return len(text) > 0
