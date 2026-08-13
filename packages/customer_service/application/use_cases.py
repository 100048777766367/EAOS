import uuid

from packages.customer_service.domain.models import SupportTicket

"""Application use cases for Customer Service and Support Handling."""


class OpenSupportTicketUseCase:
    """Use case processing customer service ticket creation."""

    def execute(self, customer_id: str, issue_summary: str) -> SupportTicket:
        """Creates a new support ticket."""
        t_id = f"TCK-{uuid.uuid4().hex[:8].upper()}"
        return SupportTicket(
            ticket_id=t_id,
            customer_id=customer_id,
            issue_summary=issue_summary,
            priority="HIGH",
            status="OPEN",
        )
