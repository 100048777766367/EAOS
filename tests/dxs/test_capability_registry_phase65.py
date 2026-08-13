from dxs.ai.capability import Capability
from dxs.application.capability_registry_service import (
    CapabilityRegistryService,
)


def test_capability_registry_is_deterministic() -> None:
    registry = CapabilityRegistryService(
        capabilities=(
            Capability(
                name="vision",
                description="Vision capability",
            ),
            Capability(
                name="text",
                description="Text capability",
            ),
        )
    )

    assert registry.has("vision")
    assert registry.has("text")
    assert [item.name for item in registry.list()] == [
        "text",
        "vision",
    ]


def test_capability_registry_rejects_duplicate() -> None:
    capability = Capability(
        name="text",
        description="Text capability",
    )

    registry = CapabilityRegistryService(capabilities=(capability,))

    try:
        registry.register(capability)
    except ValueError as exc:
        assert "already registered" in str(exc)
    else:
        raise AssertionError("Duplicate capability was accepted.")
