"""Service health inspector and deployable unit auditor for EAOS."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict


class ServiceUnitStatusDTO(BaseModel):
    """Value object representing deployable service unit health."""

    model_config = ConfigDict(frozen=True)

    service_name: str
    app_path: str
    status: str
    health_check_passed: bool


class ServiceHealthInspector:
    """Inspector auditing deployable microservice units across services/."""

    SERVICES: tuple[str, ...] = (
        "ai-service",
        "analytics-service",
        "api-gateway",
        "automation-service",
        "identity-service",
        "knowledge-service",
        "search-service",
        "workflow-service",
    )

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()
        self.services_dir: Path = self.root_dir / "services"

    def inspect_all_services(self) -> list[ServiceUnitStatusDTO]:
        """Audits all deployable service unit entrypoints in services/."""
        results: list[ServiceUnitStatusDTO] = []
        if not self.services_dir.exists():
            return results

        for service_name in self.SERVICES:
            svc_dir = self.services_dir / service_name
            app_file = svc_dir / "app.py"
            exists = app_file.exists()

            results.append(
                ServiceUnitStatusDTO(
                    service_name=service_name,
                    app_path=str(app_file.relative_to(self.root_dir) if exists else f"services/{service_name}/app.py"),
                    status="DEPLOYABLE" if exists else "MISSING",
                    health_check_passed=exists,
                )
            )

        return results
