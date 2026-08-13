"""Abstract interface for EAOS LLM adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any


class BaseLLMAdapter(ABC):
    """Abstract interface for streaming LLM adapters."""

    @abstractmethod
    def generate_stream(
        self,
        messages: list[dict[str, Any]],
        temperature: float = 0.7,
        max_output_tokens: int = 4096,
        json_mode: bool = False,
    ) -> AsyncIterator[str]:
        """Stream generated text."""
        raise NotImplementedError
