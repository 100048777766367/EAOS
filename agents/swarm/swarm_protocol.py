from __future__ import annotations

"""Giao thức truyền thông điệp Swarm Message Bus."""


class SwarmProtocol:
    """Quản lý giao tiếp đa Agent."""

    def broadcast_message(self, sender: str, message: str) -> bool:
        """Phát sóng thông điệp tới toàn bộ Swarm."""
        return len(sender) > 0 and len(message) > 0
