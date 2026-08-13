from __future__ import annotations

"""Động cơ ứng dụng Web SPA Dashboard."""


class WebAppEngine:
    """Khởi chạy Web SPA Dashboard Server."""

    def start_web_server(self, port: int = 8000) -> str:
        """Khởi chạy Web Server."""
        return f"http://127.0.0.1:{port}/chat"
