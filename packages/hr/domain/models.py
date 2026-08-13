from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""People & HR Management Domain Model for EAOS."""


class EmployeeProfile(BaseModel):
    """Value object representing an employee or AI agent operator."""

    model_config = ConfigDict(frozen=True)

    employee_id: str = Field(..., description="Unique Employee ID")
    full_name: str = Field(..., description="Employee full name")
    role_title: str = Field(..., description="Organizational role")
    department: str = Field(default="OPERATIONS")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
