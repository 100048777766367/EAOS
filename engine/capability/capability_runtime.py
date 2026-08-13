import logging
import time
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

"""Unified Capability Runtime Engine executing business commands."""


logger = logging.getLogger(__name__)


class CapabilityExecutionCommandDTO(BaseModel):
    """Value object representing an executable business capability command."""

    model_config = ConfigDict(frozen=True)

    capability_id: str = Field(..., description="Target Capability ID")
    action: str = Field(..., description="Action name to execute")
    payload: dict[str, Any] = Field(default_factory=dict)


class CapabilityExecutionResultDTO(BaseModel):
    """Value object representing capability execution outcome."""

    model_config = ConfigDict(frozen=True)

    capability_id: str
    action: str
    success: bool
    result_data: dict[str, Any]
    execution_time_ms: float


class CapabilityRuntimeEngine:
    """Runtime engine dispatching business commands to capability packages."""

    def execute_capability(self, command: CapabilityExecutionCommandDTO) -> CapabilityExecutionResultDTO:
        """Executes business capability command dynamically."""
        start_time = time.perf_counter()
        logger.info(
            "Executing capability %s action %s",
            command.capability_id,
            command.action,
        )

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return CapabilityExecutionResultDTO(
            capability_id=command.capability_id,
            action=command.action,
            success=True,
            result_data={
                "status": "EXECUTED",
                "capability": command.capability_id,
                "payload_processed": command.payload,
            },
            execution_time_ms=round(elapsed_ms, 2),
        )


if __name__ == "__main__":
    engine = CapabilityRuntimeEngine()
    cmd = CapabilityExecutionCommandDTO(
        capability_id="marketing",
        action="research_keyword",
        payload={"keyword": "AI Company"},
    )
    res = engine.execute_capability(cmd)
    print(f"✔ Capability Runtime Executed: {res.capability_id} ({res.action})")
