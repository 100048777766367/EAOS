from pydantic import BaseModel, ConfigDict

"""WCAG 2.1 Accessibility Color Contrast Auditor."""


class WCAGAuditResult(BaseModel):
    """Color contrast ratio evaluation result."""

    model_config = ConfigDict(frozen=True)

    color_fg: str
    color_bg: str
    contrast_ratio: float
    passes_aa_normal: bool
    passes_aa_large: bool
    passes_aaa_normal: bool


class WCAGAuditor:
    """Audits color contrast ratios against W3C WCAG 2.1 standards."""

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> tuple[float, float, float]:
        hex_clean = hex_color.lstrip("#")
        if len(hex_clean) == 3:
            hex_clean = "".join([c * 2 for c in hex_clean])
        r = int(hex_clean[0:2], 16) / 255.0
        g = int(hex_clean[2:4], 16) / 255.0
        b = int(hex_clean[4:6], 16) / 255.0
        return r, g, b

    @classmethod
    def _relative_luminance(cls, hex_color: str) -> float:
        r, g, b = cls._hex_to_rgb(hex_color)
        channels = []
        for c in (r, g, b):
            if c <= 0.03928:
                channels.append(c / 12.92)
            else:
                channels.append(((c + 0.055) / 1.055) ** 2.4)
        return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]

    @classmethod
    def audit_contrast(cls, fg_hex: str, bg_hex: str) -> WCAGAuditResult:
        """Calculates contrast ratio and verifies AA/AAA compliance."""
        lum1 = cls._relative_luminance(fg_hex)
        lum2 = cls._relative_luminance(bg_hex)
        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)
        ratio = round((lighter + 0.05) / (darker + 0.05), 2)

        return WCAGAuditResult(
            color_fg=fg_hex,
            color_bg=bg_hex,
            contrast_ratio=ratio,
            passes_aa_normal=ratio >= 4.5,
            passes_aa_large=ratio >= 3.0,
            passes_aaa_normal=ratio >= 7.0,
        )
