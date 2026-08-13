"""Trình phân tích Markdown Specification."""

from __future__ import annotations


class MarkdownSpecParser:
    """Đọc và trích xuất tiêu đề đặc tả."""

    @staticmethod
    def parse_markdown_headers(content: str) -> list[str]:
        """Trích xuất các tiêu đề # trong Markdown."""
        return [
            line.strip()
            for line in content.splitlines()
            if line.startswith("#")
        ]
