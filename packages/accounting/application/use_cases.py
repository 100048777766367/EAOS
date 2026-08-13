import uuid

from packages.accounting.domain.models import GeneralLedgerRecord

"""Application use cases for Accounting General Ledger."""


class PostLedgerRecordUseCase:
    """Use case posting debit/credit entry into general ledger."""

    def execute(self, account_code: str, debit: float, credit: float) -> GeneralLedgerRecord:
        """Posts double-entry accounting record."""
        r_id = f"GL-{uuid.uuid4().hex[:8].upper()}"
        return GeneralLedgerRecord(
            record_id=r_id,
            account_code=account_code,
            debit_usd=debit,
            credit_usd=credit,
        )
