from __future__ import annotations

"""Động cơ lập kế hoạch ai."""


class PlannerEngine:
    """Sắp xếp thứ tự thực thi task."""

    def build_plan(self, tasks: list[str]) -> list[str]:
        """Xây dựng kế hoạch thực thi."""
        return sorted(tasks)
