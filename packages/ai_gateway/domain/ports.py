from typing import Protocol

from packages.ai_gateway.domain.models import LLMRequestDTO, LLMResponseDTO

"""Ports defining abstract interfaces for AI LLM Providers."""


class LLMProviderPort(Protocol):
    """Port defining abstract execution interface for LLM providers."""

    async def generate(self, request: LLMRequestDTO) -> LLMResponseDTO:
        """Generates text from LLM provider."""
        ...

    async def health_check(self) -> bool:
        """Checks health status of the provider service."""
        ...
