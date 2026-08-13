from __future__ import annotations

from typing import Any

"""Mô phỏng dựng tài sản an toàn."""


class DryRunAssetsSimulator:
    """Mô phỏng dựng tài sản."""

    @staticmethod
    def simulate_render(asset_name: str, asset_type: str) -> dict[str, Any]:
        """Chạy thử mô phỏng dựng tài sản."""
        return {
            "asset_name": asset_name,
            "asset_type": asset_type,
            "render_status": "SIMULATED_SUCCESSFUL",
        }
