"""In-memory multi-turn conversation store."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ChatMessage(BaseModel):
    """Single conversation message."""

    model_config = ConfigDict(frozen=True)

    role: str
    content: str


class Conversation(BaseModel):
    """Conversation containing ordered messages."""

    model_config = ConfigDict(frozen=True)

    conversation_id: str
    messages: list[ChatMessage] = Field(default_factory=list)


class ConversationStore:
    """Manage conversation history for the running API process."""

    def __init__(self) -> None:
        """Initialize the conversation store."""
        self._store: dict[str, list[ChatMessage]] = {}

    def get_history(
        self,
        conversation_id: str,
    ) -> list[ChatMessage]:
        """Return a copy of the conversation history."""
        return list(self._store.get(conversation_id, []))

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
    ) -> None:
        """Append one message to a conversation."""
        if conversation_id not in self._store:
            self._store[conversation_id] = []

        self._store[conversation_id].append(
            ChatMessage(
                role=role,
                content=content,
            )
        )

    def clear(self, conversation_id: str) -> None:
        """Delete one conversation."""
        self._store.pop(conversation_id, None)
