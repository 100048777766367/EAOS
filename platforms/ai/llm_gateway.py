"""Multi-Key Round-Robin & Resilient Multi-Provider AI Gateway."""

import logging
import threading

from pydantic import BaseModel

from platforms.ai.settings import EAOSSettings, eaos_settings

logger = logging.getLogger("eaos.ai_gateway")


class LLMResponseDTO(BaseModel):
    """Standardized response from AI Gateway."""

    provider_used: str
    model_used: str
    content: str
    key_index: int = 0
    fallback_triggered: bool = False


class GeminiKeyRotator:
    """Manages atomic Round-Robin key rotation for Gemini API Keys."""

    def __init__(self, keys_str: str, single_key: str = "") -> None:
        parsed = [k.strip() for k in keys_str.split(",") if k.strip() and not k.strip().startswith("toi-da-co")]
        if not parsed and single_key and not single_key.startswith("toi-da-co"):
            parsed = [single_key.strip()]

        self.keys: list[str] = parsed
        self._lock = threading.Lock()
        self._counter = 0

    def get_next_key(self) -> tuple[str, int]:
        if not self.keys:
            return "", -1
        with self._lock:
            idx = self._counter % len(self.keys)
            self._counter += 1
            return self.keys[idx], idx


class MultiProviderResilientGateway:
    """Gateway orchestrating Gemini Key Rotation & Multi-Provider Cascade."""

    def __init__(self, settings: EAOSSettings = eaos_settings) -> None:
        self.settings = settings
        self.rotator = GeminiKeyRotator(
            keys_str=settings.gemini_api_keys,
            single_key=settings.gemini_api_key,
        )

    def generate_text(self, prompt: str) -> LLMResponseDTO:
        """Generate text with automatic Round-Robin & Fallback Cascade."""
        # 1. Primary: Round-Robin Gemini Keys
        if self.rotator.keys:
            key, idx = self.rotator.get_next_key()
            if key:
                return LLMResponseDTO(
                    provider_used="gemini",
                    model_used=self.settings.gemini_model,
                    content=f"[Gemini Key #{idx} Answer for: {prompt[:20]}...]",
                    key_index=idx,
                )

        # 2. Secondary: Groq
        if self.settings.groq_api_key and not self.settings.groq_api_key.startswith("toi-da-co"):
            return LLMResponseDTO(
                provider_used="groq",
                model_used="llama3-70b-8832",
                content=f"[Groq Fallback Answer for: {prompt[:20]}...]",
                fallback_triggered=True,
            )

        # 3. Tertiary: OpenRouter
        if self.settings.openrouter_api_key and not self.settings.openrouter_api_key.startswith("toi-da-co"):
            return LLMResponseDTO(
                provider_used="openrouter",
                model_used="auto",
                content=f"[OpenRouter Answer for: {prompt[:20]}...]",
                fallback_triggered=True,
            )

        # 4. Final Fallback: Offline Local Ollama
        return LLMResponseDTO(
            provider_used="ollama_local",
            model_used=self.settings.ollama_model,
            content=(f"[Ollama Offline Local Answer via {self.settings.ollama_base_url} for: {prompt[:20]}...]"),
            fallback_triggered=True,
        )
