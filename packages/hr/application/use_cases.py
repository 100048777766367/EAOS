import uuid

from packages.hr.domain.models import EmployeeProfile

"""Application use cases for HR & People Management."""


class OnboardEmployeeUseCase:
    """Use case processing new employee or AI operator onboarding."""

    def execute(self, full_name: str, role_title: str) -> EmployeeProfile:
        """Executes employee onboarding workflow."""
        emp_id = f"EMP-{uuid.uuid4().hex[:8].upper()}"
        return EmployeeProfile(
            employee_id=emp_id,
            full_name=full_name,
            role_title=role_title,
            department="OPERATIONS",
        )
