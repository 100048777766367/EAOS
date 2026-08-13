from pydantic import BaseModel, ConfigDict

"""Memory Application DTOs."""


class StoreMemoryCommand(BaseModel):
    """Command payload for storing memory."""

    model_config = ConfigDict(frozen=True)

    decision_id: str
    outcome: str
    evidence_summary: str
    lesson_learned: str
    key_learnings: list[str]


class MemoryResponse(BaseModel):
    """Response payload for memory operations."""

    model_config = ConfigDict(frozen=True)

    id: str
    outcome: str
    lesson_learned: str
    message: str = "Memory record stored successfully"
