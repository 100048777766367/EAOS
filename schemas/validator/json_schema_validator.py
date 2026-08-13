"""Trình xác thực cấu trúc JSON Schema."""

from __future__ import annotations

from typing import Any


class JsonSchemaValidator:
    """Xác thực cấu trúc JSON thuần Python."""

    @staticmethod
    def validate(schema: dict[str, Any], instance: dict[str, Any]) -> list[str]:
        """Kiểm tra các trường bắt buộc."""
        required = schema.get("required", [])
        return [f"Thiếu trường bắt buộc: '{req}'" for req in required if req not in instance]
