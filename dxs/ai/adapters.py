from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class AIRequest:
    """Provider-neutral AI request."""

    capability: str
    prompt: str

    def __post_init__(self) -> None:
        if not self.capability.strip():
            raise ValueError("AI capability must not be empty.")

        if not self.prompt.strip():
            raise ValueError("AI prompt must not be empty.")


@dataclass(frozen=True)
class AIResponse:
    """Provider-neutral AI response."""

    adapter: str
    content: str


class AIAdapter(ABC):
    """Port implemented by concrete AI providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the stable adapter name."""

    @abstractmethod
    def supports(self, capability: str) -> bool:
        """Return whether the adapter supports a capability."""

    @abstractmethod
    def execute(self, request: AIRequest) -> AIResponse:
        """Execute a provider-neutral AI request."""
