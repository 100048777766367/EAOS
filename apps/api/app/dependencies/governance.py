"""Governance FastAPI Dependencies."""

from typing import Any


def get_governance_context() -> dict[str, Any]:
    """Dependency returning current governance context."""
    return {"status": "ACTIVE", "constitution": "ARCHITECTURE_CONSTITUTION.md v3.0"}
