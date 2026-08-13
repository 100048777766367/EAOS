import uuid

from packages.product.domain.models import ProductCatalogItem

"""Application use cases for Product Management."""


class RegisterProductUseCase:
    """Use case registering digital product into enterprise catalog."""

    def execute(self, name: str, price_usd: float) -> ProductCatalogItem:
        """Registers new product item."""
        prod_id = f"PROD-{uuid.uuid4().hex[:8].upper()}"
        return ProductCatalogItem(
            product_id=prod_id,
            name=name,
            price_usd=price_usd,
            product_type="DIGITAL_TEMPLATE",
        )
