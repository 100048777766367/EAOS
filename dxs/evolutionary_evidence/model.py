from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvolutionaryEvidence:
    """Evidence that supports an evolution decision."""

    key: str
    observation: str
    outcome: str

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ValueError("Evidence key must not be empty.")

        if not self.observation.strip():
            raise ValueError("Evidence observation must not be empty.")

        if not self.outcome.strip():
            raise ValueError("Evidence outcome must not be empty.")
