"""Scope Guard Implementation for Action Control Plane."""

from __future__ import annotations


class ScopeViolationError(Exception):
    """Raised when an action violates system execution scope boundaries."""


class ScopeGuard:
    """Guard component checking action scope permissions."""

    def validate_scope(self, action_target: str, allowed_scopes: list[str] | None = None) -> bool:
        """Validates whether an action target is within allowed scopes."""
        if not allowed_scopes:
            return True
        return action_target in allowed_scopes
