from __future__ import annotations

"""Động cơ kiểm toán CQRS Commands."""


class CommandEngine:
    """Xác minh Command handler."""

    def verify_command(self, command_name: str) -> bool:
        """Kiểm tra Command hợp lệ."""
        return command_name.endswith("Command")
