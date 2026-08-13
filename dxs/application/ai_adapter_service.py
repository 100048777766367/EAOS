from __future__ import annotations

from dxs.ai.adapters import AIAdapter, AIRequest, AIResponse


class AIAdapterService:
    """Application service for provider-neutral AI adapter dispatch."""

    def __init__(
        self,
        adapters: tuple[AIAdapter, ...] = (),
    ) -> None:
        self._adapters: dict[str, AIAdapter] = {}

        for adapter in adapters:
            self.register(adapter)

    def register(self, adapter: AIAdapter) -> None:
        """Register an adapter by its stable name."""
        name = adapter.name.strip()

        if not name:
            raise ValueError("AI adapter name must not be empty.")

        if name in self._adapters:
            raise ValueError(f"AI adapter already registered: {name}")

        self._adapters[name] = adapter

    def has(self, name: str) -> bool:
        """Return whether an adapter is registered."""
        return name.strip() in self._adapters

    def list(self) -> tuple[AIAdapter, ...]:
        """Return registered adapters deterministically."""
        return tuple(self._adapters[name] for name in sorted(self._adapters))

    def execute(self, request: AIRequest) -> AIResponse:
        """Dispatch a request to the first supporting adapter."""
        for adapter in self.list():
            if adapter.supports(request.capability):
                return adapter.execute(request)

        raise LookupError(f"No registered AI adapter supports capability: {request.capability}")
