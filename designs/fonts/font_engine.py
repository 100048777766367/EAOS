from pydantic import BaseModel, ConfigDict

"""Font Registration and CSS @font-face Generator."""


class FontSpec(BaseModel):
    """Font specification model."""

    model_config = ConfigDict(frozen=True)

    family: str
    file_name: str
    format: str = "woff2"
    weight: str = "400"
    style: str = "normal"


class FontEngine:
    """Manages font registration and CSS @font-face rules."""

    def __init__(self) -> None:
        self.fonts: list[FontSpec] = []

    def register_font(self, font: FontSpec) -> None:
        """Registers a custom font spec."""
        self.fonts.append(font)

    def generate_font_face_css(self) -> str:
        """Generates CSS @font-face rules for registered fonts."""
        css_blocks = []
        for f in self.fonts:
            block = (
                f"@font-face {{\n"
                f"  font-family: '{f.family}';\n"
                f"  src: url('/fonts/{f.file_name}') format('{f.format}');\n"
                f"  font-weight: {f.weight};\n"
                f"  font-style: {f.style};\n"
                f"  font-display: swap;\n"
                f"}}"
            )
            css_blocks.append(block)
        return "\n\n".join(css_blocks)
