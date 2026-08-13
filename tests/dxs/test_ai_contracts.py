from dxs.ai.capability import Capability, CapabilityRegistrySnapshot


def test_capability_contract() -> None:
    capability = Capability(
        name="text",
        description="Text generation capability",
    )

    assert capability.name == "text"
    assert capability.description == "Text generation capability"


def test_capability_registry_snapshot() -> None:
    capability = Capability(
        name="text",
        description="Text generation capability",
    )

    snapshot = CapabilityRegistrySnapshot(
        capabilities=(capability,),
    )

    assert snapshot.capabilities == (capability,)
