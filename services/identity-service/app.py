"""SSO IAM & Authentication Provider deployable unit entry point."""

from pydantic import BaseModel, ConfigDict


class ServiceHealthResponseDTO(BaseModel):
    """Value object representing service health response."""

    model_config = ConfigDict(frozen=True)

    service_name: str
    status: str
    version: str


class identityServiceApp:
    """Deployable unit application controller for identity-service."""

    def __init__(self) -> None:
        self.service_name: str = "identity-service"

    def get_health_status(self) -> ServiceHealthResponseDTO:
        """Returns health status for deployable service."""
        return ServiceHealthResponseDTO(
            service_name=self.service_name,
            status="HEALTHY",
            version="0.1.0",
        )
