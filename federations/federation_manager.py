from __future__ import annotations

from .bft.synod_bft import SynodBft

"""Federation manager."""


class FederationManager:
    """Federation manager."""

    def __init__(self) -> None:
        self.bft = SynodBft()
