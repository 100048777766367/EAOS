from __future__ import annotations

import pytest
from dxs.ai.adapters import AIRequest
from dxs.ai.policy import (
    AIPolicy,
    PolicyDecision,
)
from dxs.application.ai_policy_service import AIPolicyService


def make_request(
    capability: str = "text-generation",
    prompt: str = "hello",
) -> AIRequest:
    return AIRequest(
        capability=capability,
        prompt=prompt,
    )


def test_allowed_capability_is_allowed() -> None:
    service = AIPolicyService(AIPolicy(allowed_capabilities=frozenset({"text-generation"})))

    result = service.evaluate(make_request())

    assert result.decision is PolicyDecision.ALLOW
    assert result.allowed is True


def test_disallowed_capability_is_denied() -> None:
    service = AIPolicyService(AIPolicy(allowed_capabilities=frozenset({"vision"})))

    result = service.evaluate(make_request())

    assert result.decision is PolicyDecision.DENY
    assert result.allowed is False
    assert "not allowed" in result.reason


def test_disabled_policy_denies_request() -> None:
    service = AIPolicyService(
        AIPolicy(
            allowed_capabilities=frozenset({"text-generation"}),
            enabled=False,
        )
    )

    result = service.evaluate(make_request())

    assert result.decision is PolicyDecision.DENY
    assert result.reason == "AI policy is disabled."


def test_prompt_length_is_enforced() -> None:
    service = AIPolicyService(
        AIPolicy(
            allowed_capabilities=frozenset({"text-generation"}),
            max_prompt_length=5,
        )
    )

    result = service.evaluate(make_request(prompt="123456"))

    assert result.decision is PolicyDecision.DENY
    assert "exceeds" in result.reason


def test_authorize_allows_valid_request() -> None:
    service = AIPolicyService(AIPolicy(allowed_capabilities=frozenset({"text-generation"})))

    service.authorize(make_request())


def test_authorize_rejects_invalid_request() -> None:
    service = AIPolicyService(AIPolicy(allowed_capabilities=frozenset({"vision"})))

    with pytest.raises(
        PermissionError,
        match="not allowed",
    ):
        service.authorize(make_request())


def test_empty_allowed_capabilities_are_normalized() -> None:
    policy = AIPolicy(allowed_capabilities=frozenset({"", "  ", "vision"}))

    assert policy.allowed_capabilities == frozenset({"vision"})


def test_invalid_prompt_limit_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="greater than zero",
    ):
        AIPolicy(
            allowed_capabilities=frozenset({"text-generation"}),
            max_prompt_length=0,
        )
