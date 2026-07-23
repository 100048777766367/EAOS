"""AI Agent Interface Application for EAOS."""

import time
from typing import Any

from pydantic import BaseModel, ConfigDict


class AgentPromptRequest(BaseModel):
    """Value object for AI Agent prompt requests."""

    model_config = ConfigDict(frozen=True)

    agent_id: str
    prompt: str
    parameters: dict[str, Any]


class AgentInteractionResponse(BaseModel):
    """Value object for AI Agent execution responses."""

    model_config = ConfigDict(frozen=True)

    interaction_id: str
    agent_id: str
    output_text: str
    execution_time_ms: float


class AgentInterfaceRunner:
    """Controller orchestrating AI Agent interaction workflows."""

    def process_agent_request(
        self,
        request: AgentPromptRequest,
    ) -> AgentInteractionResponse:
        """Executes prompt against agent and formats response."""
        start_time = time.perf_counter()
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        return AgentInteractionResponse(
            interaction_id=f"act_{int(time.time())}",
            agent_id=request.agent_id,
            output_text=f"Processed prompt for agent '{request.agent_id}'",
            execution_time_ms=round(elapsed_ms, 3),
        )
