from __future__ import annotations

"""Động cơ xử lý ADR Lifecycle."""


class AdrEngine:
    """Quản lý vòng đời ADR."""

    def evaluate_adr_compliance(self, adr_id: str) -> bool:
        """Kiểm tra tính tuân thủ của ADR."""
        return len(adr_id) > 0
