"""Legacy compatibility facade for the canonical EAOS harness."""

from __future__ import annotations

from packages.harness.enterprise_harness import (
    EAOSAgentHarnessControlPlane,
)

EAOSAgentHarness = EAOSAgentHarnessControlPlane


__all__ = [
    "EAOSAgentHarness",
    "EAOSAgentHarnessControlPlane",
]
