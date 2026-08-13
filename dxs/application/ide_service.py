from __future__ import annotations

from pathlib import Path

from dxs.domain.ide import IdeCheck, IdeReport


class IdeService:
    """Application service for IDE environment inspection."""

    def inspect(self, root: Path) -> IdeReport:
        """Inspect supported IDE configuration locations."""
        vscode = root / ".vscode"
        idea = root / ".idea"

        checks = (
            IdeCheck(
                name=".vscode",
                path=str(vscode),
                exists=vscode.is_dir(),
            ),
            IdeCheck(
                name=".idea",
                path=str(idea),
                exists=idea.is_dir(),
            ),
        )

        return IdeReport(checks=checks)
