from __future__ import annotations

from dataclasses import replace

from .model import Remediation, RemediationStatus


class RemediationService:
    """Deterministic remediation lifecycle service."""

    def create(
        self,
        key: str,
        description: str,
    ) -> Remediation:
        """Create an open remediation."""
        return Remediation(
            key=key.strip(),
            description=description.strip(),
        )

    def resolve(self, remediation: Remediation) -> Remediation:
        """Resolve a remediation."""
        return replace(
            remediation,
            status=RemediationStatus.RESOLVED,
        )

    def block(self, remediation: Remediation) -> Remediation:
        """Mark a remediation as blocked."""
        return replace(
            remediation,
            status=RemediationStatus.BLOCKED,
        )
