from typing import Protocol
from domain.models import Invoice


class InvoiceRepository(Protocol):
    """Port tự động sinh bởi Architecture Compiler."""

    def save(self, entity: Invoice) -> Invoice: ...

    def find_by_id(self, entity_id: str) -> Invoice | None: ...

