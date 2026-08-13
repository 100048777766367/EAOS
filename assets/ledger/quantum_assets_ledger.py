from __future__ import annotations

import hashlib
import json
import time
from typing import Any

"""Sổ cái vết tài sản trực quan chống lượng tử."""


class QuantumAssetsLedger:
    """Đúc bằng chứng mã hóa tài sản trực quan."""

    @staticmethod
    def generate_asset_proof(
        asset_id: str,
        payload: dict[str, Any],
        secret_key: str = "EAOS_ASSETS_PQ_2026",
    ) -> str:
        """Sinh mã băm chứng nhận tài sản không thể sửa đổi."""
        serialized = json.dumps(payload, sort_keys=True)
        timestamp = str(time.time_ns())
        raw_bytes = f"{asset_id}:{serialized}:{timestamp}:{secret_key}".encode()
        hasher = hashlib.sha3_256()
        hasher.update(raw_bytes)
        return f"pq_asset_{hasher.hexdigest()}"
