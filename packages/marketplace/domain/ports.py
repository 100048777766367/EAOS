from typing import Protocol

from packages.marketplace.domain.models import MarketplaceAsset
from packages.memory.domain.entities import MemoryRecord  # Sửa đúng dòng này


class MarketplacePort(Protocol):
    """Port định nghĩa hành vi đăng bán, tìm kiếm và cắm nóng Capability."""

    def publish_asset(self, asset: MarketplaceAsset) -> MarketplaceAsset: ...

    def find_asset_by_id(self, asset_id: str) -> MarketplaceAsset | None: ...

    def list_assets(self) -> list[MarketplaceAsset]: ...