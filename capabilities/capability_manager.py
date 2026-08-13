from __future__ import annotations

from .capability_registry import CapabilityRegistry
from .ledger.quantum_capability_ledger import QuantumCapabilityLedger

"""Capability manager module."""


class CapabilityManager:
    """Capability manager."""

    def __init__(self) -> None:
        self.registry = CapabilityRegistry()
        self.ledger = QuantumCapabilityLedger()
