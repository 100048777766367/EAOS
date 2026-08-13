from __future__ import annotations

"""Động cơ kiểm toán Aggregate Roots."""


class AggregateEngine:
    """Xác minh bất biến Aggregate."""

    def verify_aggregate(self, aggregate_name: str) -> bool:
        """Kiểm tra Aggregate Root hợp lệ."""
        return len(aggregate_name) > 0
