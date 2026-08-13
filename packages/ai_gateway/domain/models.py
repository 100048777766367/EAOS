from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""AI Gateway Domain Models and Exceptions for EAOS."""


class AIProviderTimeoutError(Exception):
    """Domain exception raised when AI provider request times out."""


class AIProviderUnavailableError(Exception):
    """Domain exception raised when AI provider service is down."""


class LLMRequestDTO(BaseModel):
    """Value object representing an LLM execution request."""

    model_config = ConfigDict(frozen=True)

    prompt: str = Field(..., description="User prompt string")
    model: str = Field(default="llama3", description="Target model name")
    temperature: float = Field(default=0.2)
    max_tokens: int = Field(default=1024)


class LLMResponseDTO(BaseModel):
    """Value object representing a structured LLM response."""

    model_config = ConfigDict(frozen=True)

    content: str = Field(..., description="Generated text content")
    provider: str = Field(..., description="Provider name")
    model_used: str = Field(..., description="Actual model used")
    tokens_used: int = Field(default=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
