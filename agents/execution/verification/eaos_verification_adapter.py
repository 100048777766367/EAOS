"""Adapter for the existing EAOS verification coordinator."""

from __future__ import annotations

from pathlib import Path
from typing import Any


class EAOSVerificationAdapter:
    """Connect agent execution to EAOS verification."""

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root.resolve()

    async def verify(self) -> dict[str, Any]:
        """Run existing verification coordinator."""
        from apps.api.app.services.chat.verification.coordinator import (
            VerificationCoordinator,
        )

        coordinator = VerificationCoordinator(self.project_root)

        events: list[dict[str, Any]] = []
        final: dict[str, Any] | None = None

        async for event in coordinator.run():
            events.append(event)

            if event.get("type") == "verification_result":
                final = event

        if final is None:
            raise RuntimeError("Verification coordinator produced no result.")

        return {
            "result": final,
            "events": events,
        }
