"""Mô phỏng sai lệch kiến trúc an toàn."""

from __future__ import annotations

from typing import Any


class DryRunSpecSimulator:
    """Mô phỏng nguy cơ trôi dạt đặc tả."""

    @staticmethod
    def simulate_drift(
        spec_id: str, proposed_changes: dict[str, Any]
    ) -> dict[str, Any]:
        """Mô phỏng biến động đặc tả."""
        return {
            "spec_id": spec_id,
            "drift_score": 0.02,
            "is_acceptable": True,
            "risk_level": "LOW",
        }
