import json
import re
from pathlib import Path
from typing import Self

from pydantic import BaseModel, Field, model_validator

"""Design Token Compiler Engine for EAOS Design System."""


class ColorToken(BaseModel):
    """Mô hình dữ liệu Token Màu sắc."""

    hex_value: str = Field(alias="hex")
    description: str = ""

    @model_validator(mode="after")
    def validate_hex(self) -> Self:
        """Kiểm tra mã HEX hợp lệ theo định dạng CSS."""
        val = self.hex_value.lstrip("#")
        if not re.match(r"^[0-9a-fA-F]{6}$", val):
            raise ValueError(f"Mã HEX không hợp lệ: {self.hex_value}")
        return self


class ColorPalette(BaseModel):
    """Bộ Bảng màu Chuẩn của Hệ thống."""

    primary: ColorToken
    background: ColorToken
    surface: ColorToken
    text_main: ColorToken = Field(alias="textMain")
    text_muted: ColorToken = Field(alias="textMuted")
    danger: ColorToken
    success: ColorToken


class DesignTokenCompiler:
    """Động cơ biên dịch Tokens sang CSS Variables và TypeScript Types."""

    def __init__(self, tokens_dir: Path) -> None:
        self.tokens_dir = tokens_dir

    def load_palette(self) -> ColorPalette:
        """Nạp tệp JSON màu sắc và validate bằng Pydantic v2."""
        file_path = self.tokens_dir / "colors.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Không tìm thấy tệp token: {file_path}")

        data = json.loads(file_path.read_text(encoding="utf-8"))
        return ColorPalette.model_validate(data)

    def compile_to_css_variables(self, palette: ColorPalette) -> str:
        """Biên dịch palette màu sang tập CSS Variables."""
        css_lines = [
            ":root {",
            f"  --color-primary: {palette.primary.hex_value};",
            f"  --color-background: {palette.background.hex_value};",
            f"  --color-surface: {palette.surface.hex_value};",
            f"  --color-text-main: {palette.text_main.hex_value};",
            f"  --color-text-muted: {palette.text_muted.hex_value};",
            f"  --color-danger: {palette.danger.hex_value};",
            f"  --color-success: {palette.success.hex_value};",
            "}",
        ]
        return "\n".join(css_lines)

    def compile_to_typescript_types(self, palette: ColorPalette) -> str:
        """Biên dịch palette màu sang kiểu dữ liệu TypeScript Type Definition."""
        keys = list(palette.model_dump().keys())
        union_keys = " | ".join([f'"{k}"' for k in keys])
        return f"export type EAOSColorTokenKey = {union_keys};\n"
