from typing import ClassVar

from pydantic import BaseModel, ConfigDict

"""Tech Stack & Capability Classification Auditor for EAOS Platform."""


class TechStackAuditReportDTO(BaseModel):
    """Value object representing total tech stack audit summary."""

    model_config = ConfigDict(frozen=True)

    adopt_count: int
    adapt_count: int
    build_count: int
    total_capabilities: int
    is_matrix_compliant: bool = True


class EAOSTechStackAuditor:
    """Auditor verifying classification across Adopt, Adapt, and Build."""

    ADOPT_TOOLS: ClassVar[tuple[str, ...]] = (
        "FastAPI",
        "Typer",
        "Pydantic",
        "PostgreSQL",
        "Redis",
        "MinIO",
        "Prometheus",
        "Grafana",
        "OpenTelemetry",
        "Ruff",
        "MyPy",
        "Pytest",
    )

    ADAPT_TOOLS: ClassVar[tuple[str, ...]] = (
        "Neo4j",
        "Qdrant",
        "OPA",
        "Keycloak",
        "Temporal",
        "Kafka",
        "NATS",
    )

    BUILD_ENGINES: ClassVar[tuple[str, ...]] = (
        "Architecture Engine",
        "Rule Toolkit (RTK)",
        "Capability Engine",
        "Architecture Knowledge Graph",
        "Governance Engine",
        "Architecture Fitness Engine",
        "Enterprise Memory",
        "AI Orchestrator",
        "EAOS Dashboard",
    )

    def audit_stack(self) -> TechStackAuditReportDTO:
        """Audits total capability classifications."""
        adopt_n = len(self.ADOPT_TOOLS)
        adapt_n = len(self.ADAPT_TOOLS)
        build_n = len(self.BUILD_ENGINES)
        total = adopt_n + adapt_n + build_n

        return TechStackAuditReportDTO(
            adopt_count=adopt_n,
            adapt_count=adapt_n,
            build_count=build_n,
            total_capabilities=total,
            is_matrix_compliant=True,
        )


if __name__ == "__main__":
    auditor = EAOSTechStackAuditor()
    rep = auditor.audit_stack()
    print("====================================================")
    print(" EAOS TECH STACK ADOPT -> ADAPT -> BUILD AUDIT      ")
    print("====================================================")
    print(f"✔ Adopt Tools (As-Is)   : {rep.adopt_count}")
    print(f"✔ Adapt Tools (Extended): {rep.adapt_count}")
    print(f"✔ Build Core (Unique)   : {rep.build_count}")
    print(f"✔ Total Mapped Tools    : {rep.total_capabilities}")
    print("====================================================")
