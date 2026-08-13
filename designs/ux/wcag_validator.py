from dataclasses import dataclass

"""WCAG 2.1 Color Contrast Ratio Auditor Engine."""


@dataclass(frozen=True, slots=True)
class WCAGContrastReport:
    """Báo cáo Đánh giá Tương phản WCAG 2.1."""

    foreground_hex: str
    background_hex: str
    contrast_ratio: float
    passes_aa_normal: bool
    passes_aa_large: bool
    passes_aaa_normal: bool


class WCAGAuditor:
    """Động cơ tính toán độ tương phản màu sắc theo tiêu chuẩn W3C WCAG 2.1."""

    @staticmethod
    def _hex_to_rgb(hex_code: str) -> tuple[int, int, int]:
        clean_hex = hex_code.lstrip("#")
        return (
            int(clean_hex[0:2], 16),
            int(clean_hex[2:4], 16),
            int(clean_hex[4:6], 16),
        )

    @staticmethod
    def calculate_relative_luminance(rgb: tuple[int, int, int]) -> float:
        """Tính độ chói tương đối (Relative Luminance) theo công thức W3C."""
        channels = []
        for channel in rgb:
            s_rgb = channel / 255.0
            c_linear = s_rgb / 12.92 if s_rgb <= 0.04045 else ((s_rgb + 0.055) / 1.055) ** 2.4
            channels.append(c_linear)

        return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]

    def audit_contrast(self, foreground_hex: str, background_hex: str) -> WCAGContrastReport:
        """Đánh giá tỷ lệ tương phản giữa hai màu HEX."""
        rgb_fg = self._hex_to_rgb(foreground_hex)
        rgb_bg = self._hex_to_rgb(background_hex)

        lum1 = self.calculate_relative_luminance(rgb_fg)
        lum2 = self.calculate_relative_luminance(rgb_bg)

        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)

        ratio = round((lighter + 0.05) / (darker + 0.05), 2)

        return WCAGContrastReport(
            foreground_hex=foreground_hex,
            background_hex=background_hex,
            contrast_ratio=ratio,
            passes_aa_normal=ratio >= 4.5,
            passes_aa_large=ratio >= 3.0,
            passes_aaa_normal=ratio >= 7.0,
        )
