from typing import Protocol

from packages.marketplace.domain.models import MarketplaceAsset


class MarketplacePort(Protocol):
    """Port Ä‘á»‹nh nghÄ©a hÃ nh vi Ä‘Äƒng bÃ¡n, tÃ¬m kiáº¿m vÃ  cáº¯m nÃ³ng Capability."""

    def publish_asset(self, asset: MarketplaceAsset) -> MarketplaceAsset: ...

    def find_asset_by_id(self, asset_id: str) -> MarketplaceAsset | None: ...

    def list_assets(self) -> list[MarketplaceAsset]: ...
