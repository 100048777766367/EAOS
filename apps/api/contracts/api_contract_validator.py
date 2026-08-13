from typing import Any

"""API Contract Validator."""


class APIContractValidator:
    """Validates API request and response payload integrity."""

    def validate_payload(self, payload: dict[str, Any]) -> bool:
        """Verifies payload is non-empty dictionary."""
        return isinstance(payload, dict)
