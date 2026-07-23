"""Platform service adapter abstracting LLM providers."""

from pydantic import BaseModel, ConfigDict


class LLMResponseDTO(BaseModel):
    """Value object representing an LLM completion response."""

    model_config = ConfigDict(frozen=True)

    model_name: str
    completion_text: str
    tokens_used: int


class LLMProviderAdapter:
    """Infrastructure adapter decoupling domain from LLM vendor SDKs."""

    def complete_prompt(
        self,
        prompt: str,
        model: str = "ollama/llama3",
    ) -> LLMResponseDTO:
        """Executes prompt completion through unified interface."""
        return LLMResponseDTO(
            model_name=model,
            completion_text=f"Completed prompt: {prompt[:30]}",
            tokens_used=len(prompt.split()),
        )
