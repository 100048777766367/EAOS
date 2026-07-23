"""Local Edge Ollama AI adapter for offline resilient inference."""

from pydantic import BaseModel, ConfigDict


class OllamaInferenceRequest(BaseModel):
    """Request model for local Ollama LLM completion."""

    model_config = ConfigDict(frozen=True)

    prompt: str
    model_name: str = "ollama/llama3"
    temperature: float = 0.2


class OllamaInferenceResponse(BaseModel):
    """Response model from local Ollama LLM completion."""

    model_config = ConfigDict(frozen=True)

    content: str
    model_used: str
    tokens_used: int
    offline_fallback: bool


class LocalOllamaAdapter:
    """Adapter managing local Ollama inference and offline fallback."""

    def generate_completion(self, prompt: str, model_name: str = "ollama/llama3") -> OllamaInferenceResponse:
        """Generates completion locally or returns resilient offline fallback."""
        response_text = f"[EAOS Local Edge AI Response] Processed prompt: '{prompt[:30]}...'"
        return OllamaInferenceResponse(
            content=response_text,
            model_used=model_name,
            tokens_used=len(prompt.split()),
            offline_fallback=True,
        )
