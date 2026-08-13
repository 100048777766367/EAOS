from dxs.ai.adapters import AIAdapter, AIRequest, AIResponse


def test_ai_adapter_contract_is_importable() -> None:
    assert AIAdapter is not None
    assert AIRequest is not None
    assert AIResponse is not None
