"""AI Capability Service and AI Gateway with Fallback and Routing."""

from packages.ai_gateway.domain.models import (
    AIProviderTimeoutError,
    AIProviderUnavailableError,
    LLMRequestDTO,
    LLMResponseDTO,
)
from packages.ai_gateway.domain.ports import LLMProviderPort


class AICapabilityService:
    """Central AI Gateway orchestrating routing, retries and fallbacks."""

    def __init__(
        self,
        primary_provider: LLMProviderPort,
        fallback_provider: LLMProviderPort | None = None,
    ) -> None:
        self.primary = primary_provider
        self.fallback = fallback_provider

    async def generate(self, request: LLMRequestDTO) -> LLMResponseDTO:
        """Executes AI generation with automatic fallback capability."""
        try:
            return await self.primary.generate(request)
        except (AIProviderTimeoutError, AIProviderUnavailableError):
            if self.fallback:
                return await self.fallback.generate(request)
            raise
