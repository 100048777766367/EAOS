import uuid

from packages.crm.domain.models import SalesLead

"""Application use cases for Sales Lead Ingestion and Scoring."""


class IngestLeadUseCase:
    """Use case processing lead capture from Marketing Funnel."""

    def execute(self, email: str, source: str) -> SalesLead:
        """Ingests new sales lead into CRM capability."""
        lead_id = f"LEAD-{uuid.uuid4().hex[:8].upper()}"
        score = 10.0 if "FUNNEL" in source else 5.0
        status_str = "QUALIFIED" if score >= 10.0 else "NEW"
        return SalesLead(
            lead_id=lead_id,
            email=email,
            source=source,
            score=score,
            status=status_str,
        )
