from __future__ import annotations

"""Động cơ bộ nhớ trượt ai."""


class MemoryEngine:
    """Lưu trữ lịch sử hội thoại trượt."""

    def __init__(self) -> None:
        self._history: list[str] = []

    def append_message(self, msg: str) -> None:
        """Thêm tin nhắn vào bộ nhớ."""
        self._history.append(msg)
