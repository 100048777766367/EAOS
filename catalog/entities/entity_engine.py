from __future__ import annotations

"""Động cơ kiểm toán DDD Entities."""


class EntityEngine:
    """Xác minh Entity Identity."""

    def verify_entity(self, entity_name: str) -> bool:
        """Kiểm tra Entity hợp lệ."""
        return len(entity_name) > 0
