from __future__ import annotations

import pytest
from dxs.ai.adapters import AIAdapter, AIRequest, AIResponse
from dxs.application.ai_adapter_service import AIAdapterService


class TextAdapter(AIAdapter):
    """Test adapter implementing the real adapter contract."""

    @property
    def name(self) -> str:
        return "text-adapter"

    def supports(self, capability: str) -> bool:
        return capability == "text-generation"

    def execute(self, request: AIRequest) -> AIResponse:
        return AIResponse(
            adapter=self.name,
            content=f"processed:{request.prompt}",
        )


class VisionAdapter(AIAdapter):
    """Test adapter for a separate capability."""

    @property
    def name(self) -> str:
        return "vision-adapter"

    def supports(self, capability: str) -> bool:
        return capability == "vision"

    def execute(self, request: AIRequest) -> AIResponse:
        return AIResponse(
            adapter=self.name,
            content=f"processed:{request.prompt}",
        )


def test_request_rejects_empty_capability() -> None:
    with pytest.raises(
        ValueError,
        match="capability must not be empty",
    ):
        AIRequest(
            capability="",
            prompt="hello",
        )


def test_request_rejects_empty_prompt() -> None:
    with pytest.raises(
        ValueError,
        match="prompt must not be empty",
    ):
        AIRequest(
            capability="text-generation",
            prompt="",
        )


def test_adapter_can_be_registered() -> None:
    service = AIAdapterService()

    service.register(TextAdapter())

    assert service.has("text-adapter") is True


def test_duplicate_adapter_is_rejected() -> None:
    service = AIAdapterService()

    service.register(TextAdapter())

    with pytest.raises(
        ValueError,
        match="already registered",
    ):
        service.register(TextAdapter())


def test_adapter_listing_is_deterministic() -> None:
    service = AIAdapterService(
        adapters=(
            VisionAdapter(),
            TextAdapter(),
        )
    )

    assert tuple(adapter.name for adapter in service.list()) == (
        "text-adapter",
        "vision-adapter",
    )


def test_request_is_dispatched_to_supporting_adapter() -> None:
    service = AIAdapterService(adapters=(TextAdapter(),))

    response = service.execute(
        AIRequest(
            capability="text-generation",
            prompt="hello",
        )
    )

    assert response.adapter == "text-adapter"
    assert response.content == "processed:hello"


def test_unsupported_capability_is_rejected() -> None:
    service = AIAdapterService(adapters=(TextAdapter(),))

    with pytest.raises(
        LookupError,
        match="No registered AI adapter supports capability",
    ):
        service.execute(
            AIRequest(
                capability="vision",
                prompt="image",
            )
        )
