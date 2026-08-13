from __future__ import annotations

"""Động cơ ứng dụng CLI Console."""


class CliAppEngine:
    """Khởi chạy CLI Console."""

    def execute_command(self, cmd: str) -> str:
        """Thực thi lệnh CLI."""
        return f"EXECUTED_{cmd}"
