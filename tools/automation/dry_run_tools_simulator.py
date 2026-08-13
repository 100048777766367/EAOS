from __future__ import annotations

from typing import Any

"""Mô phỏng chạy công cụ an toàn."""


class DryRunToolsSimulator:
    """Mô phỏng tác động thực thi công cụ."""

    @staticmethod
    def simulate_tool(tool_name: str, args: list[str]) -> dict[str, Any]:
        """Chạy thử mô phỏng công cụ."""
        return {
            "tool_name": tool_name,
            "args": args,
            "is_safe": True,
            "impact_risk": "LOW",
        }
