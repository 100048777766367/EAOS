from __future__ import annotations

"""Động cơ gọi API LLM Provider."""


class ProviderEngine:
    """Thực thi cuộc gọi API LLM."""

    def call_provider(self, model: str, prompt: str) -> str:
        """Gọi LLM Provider."""
        return f"Response from {model} for {prompt[:10]}"
