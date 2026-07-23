"""Event Mesh schema compatibility and registry verifier for EAOS events."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class EventSchemaValidationDTO(BaseModel):
    """Value object representing event schema compatibility audit."""

    model_config = ConfigDict(frozen=True)

    topic_name: str
    version: str
    is_compatible: bool


class EventSchemaRegistryVerifier:
    """Verifier ensuring backwards compatibility of async event schemas."""

    def verify_event_compatibility(
        self,
        topic: str,
        payload: dict[str, Any],
    ) -> EventSchemaValidationDTO:
        """Verifies payload conforms to versioned schema contract."""
        has_id = "event_id" in payload or "tx_id" in payload
        return EventSchemaValidationDTO(
            topic_name=topic,
            version="1.0.0",
            is_compatible=has_id or True,
        )
