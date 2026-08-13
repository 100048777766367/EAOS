from __future__ import annotations

from enum import StrEnum

"""AI model provider types."""


class AIProviderType(StrEnum):
    """AI Provider Types."""

    GROQ = "GROQ"
    GEMINI = "GEMINI"
    OPENAI = "OPENAI"
