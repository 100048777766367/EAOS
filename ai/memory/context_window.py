from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Context Window and Short-Term Memory Manager."""


class ContextWindowDTO(BaseModel):
    """Context window memory container."""

    model_config = ConfigDict(frozen=True)

    max_tokens: int = Field(default=65536)
    current_token_count: int = Field(default=0)
    system_context: str = Field(default="")
    chat_history: list[str] = Field(default_factory=list)


class ContextWindowManager:
    """Manager controlling token budget and context history."""

    def prepare_context(self, system_prompt: str, user_prompt: str) -> ContextWindowDTO:
        """Assemble system and user context within token limits."""
        estimated_tokens = len((system_prompt + user_prompt).split())
        return ContextWindowDTO(
            max_tokens=65536,
            current_token_count=estimated_tokens,
            system_context=system_prompt,
            chat_history=[user_prompt],
        )
