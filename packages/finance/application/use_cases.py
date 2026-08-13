import uuid

from packages.finance.domain.models import FinancialLedgerEntry

"""Application use cases for Financial Accounting and FinOps."""


class RecordFinancialTransactionUseCase:
    """Use case recording revenue and operational API costs."""

    def execute(self, revenue_usd: float, cost_usd: float, entry_type: str) -> FinancialLedgerEntry:
        """Calculates net margin and records financial ledger entry."""
        tx_id = f"TX-{uuid.uuid4().hex[:8].upper()}"
        margin = revenue_usd - cost_usd
        return FinancialLedgerEntry(
            transaction_id=tx_id,
            revenue_usd=revenue_usd,
            cost_usd=cost_usd,
            net_margin_usd=margin,
            entry_type=entry_type,
        )
