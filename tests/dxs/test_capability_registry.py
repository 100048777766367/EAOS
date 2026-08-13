from __future__ import annotations

import pytest
from dxs.ai.capability import Capability
from dxs.application.capability_registry_service import (
    CapabilityRegistryService,
)


def test_register_and_get_capability() -> None:
    registry = CapabilityRegistryService()

    capability = Capability(
        name="text-generation",
        description="Generate text from a prompt.",
    )

    registry.register(capability)

    assert registry.has("text-generation") is True
    assert registry.get("text-generation") == capability


def test_registry_returns_deterministic_order() -> None:
    registry = CapabilityRegistryService()

    registry.register(
        Capability(
            name="vision",
            description="Process visual input.",
        )
    )
    registry.register(
        Capability(
            name="text-generation",
            description="Generate text.",
        )
    )

    names = tuple(capability.name for capability in registry.list())

    assert names == (
        "text-generation",
        "vision",
    )


def test_duplicate_capability_is_rejected() -> None:
    registry = CapabilityRegistryService()

    capability = Capability(
        name="vision",
        description="Process visual input.",
    )

    registry.register(capability)

    with pytest.raises(ValueError, match="already registered"):
        registry.register(capability)


def test_missing_capability_is_rejected() -> None:
    registry = CapabilityRegistryService()

    with pytest.raises(
        KeyError,
        match="Capability not registered",
    ):
        registry.get("missing")


def test_empty_capability_name_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="name must not be empty",
    ):
        Capability(
            name="",
            description="Invalid capability.",
        )


def test_snapshot_is_deterministic() -> None:
    registry = CapabilityRegistryService(
        capabilities=(
            Capability(
                name="vision",
                description="Process visual input.",
            ),
            Capability(
                name="text-generation",
                description="Generate text.",
            ),
        )
    )

    snapshot = registry.snapshot()

    assert tuple(capability.name for capability in snapshot.capabilities) == (
        "text-generation",
        "vision",
    )
