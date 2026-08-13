from __future__ import annotations

from typing import Any

"""Mô phỏng khởi chạy ứng dụng an toàn."""


class DryRunAppsSimulator:
    """Mô phỏng chạy thử ứng dụng."""

    @staticmethod
    def simulate_launch(app_type: str) -> dict[str, Any]:
        """Chạy thử mô phỏng ứng dụng."""
        return {
            "app_type": app_type,
            "status": "SIMULATED_LAUNCH_SUCCESSFUL",
            "port_allocated": 8000,
        }
