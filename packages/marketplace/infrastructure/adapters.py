from packages.marketplace.domain.models import MarketplaceAsset
from packages.marketplace.domain.ports import MarketplacePort


class InMemoryMarketplace(MarketplacePort):
    """Adapter lÆ°u trá»¯ kho á»©ng dá»¥ng NÄƒng lá»±c trong RAM."""

    def __init__(self) -> None:
        self._store: dict[str, MarketplaceAsset] = {}

    def publish_asset(self, asset: MarketplaceAsset) -> MarketplaceAsset:
        self._store[asset.asset_id] = asset
        return asset

    def find_asset_by_id(self, asset_id: str) -> MarketplaceAsset | None:
        return self._store.get(asset_id)

    def list_assets(self) -> list[MarketplaceAsset]:
        return list(self._store.values())

