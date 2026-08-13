from __future__ import annotations

from pathlib import Path

from dxs.domain.integrations import (
    IntegrationCheck,
    IntegrationReport,
)


class IntegrationService:
    """Application service for integration inspection."""

    def inspect(self, root: Path) -> IntegrationReport:
        """Inspect supported integration configuration locations."""
        checks = (
            IntegrationCheck(
                name=".github",
                path=str(root / ".github"),
                exists=(root / ".github").is_dir(),
            ),
            IntegrationCheck(
                name="pyproject.toml",
                path=str(root / "pyproject.toml"),
                exists=(root / "pyproject.toml").is_file(),
            ),
        )

        return IntegrationReport(checks=checks)
