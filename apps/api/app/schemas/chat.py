"""Chat schemas for the EAOS AI Studio WebSocket pipeline."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ChatMessage(BaseModel):
    """A single message in a conversation."""

    model_config = ConfigDict(frozen=True)

    role: str = Field(
        ...,
        description="Message role: system, user, or assistant.",
    )
    content: str = Field(
        ...,
        description="Message text.",
    )


class ChatCompletionRequest(BaseModel):
    """HTTP-compatible chat completion request."""

    model_config = ConfigDict(frozen=True)

    model: str = Field(
        default="ollama",
        description="Target model identifier.",
    )
    messages: list[ChatMessage] = Field(
        default_factory=list,
        description="Conversation history.",
    )
    stream: bool = Field(
        default=False,
        description="Whether to stream the response.",
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Sampling temperature.",
    )
    max_output_tokens: int = Field(
        default=4096,
        ge=1,
        le=32768,
        description="Maximum generated tokens.",
    )
    json_mode: bool = Field(
        default=False,
        description="Request structured JSON output.",
    )


class ChatWebSocketRequest(BaseModel):
    """Request received from the EAOS AI Studio WebSocket."""

    model_config = ConfigDict(frozen=True)

    conversation_id: str = Field(
        default="default",
        min_length=1,
    )
    agent_role: str = Field(
        default="Coder Agent",
        min_length=1,
    )
    message: str = Field(
        ...,
        min_length=1,
    )
    system_instruction: str = Field(
        default="",
    )
    active_file: str = Field(
        default="",
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
    )
    max_output_tokens: int = Field(
        default=4096,
        ge=1,
        le=32768,
    )
    json_mode: bool = Field(
        default=False,
    )
