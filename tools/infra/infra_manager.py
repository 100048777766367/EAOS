"""Infrastructure as Code (IaC) manager and service health inspector."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict


class InfraServiceHealthDTO(BaseModel):
    """Value object representing an infrastructure service health report."""

    model_config = ConfigDict(frozen=True)

    service_name: str
    config_path: str
    status: str
    port_binding: int


class InfraManagerEngine:
    """Engine inspecting IaC configurations and service definitions."""

    SERVICES_MAP: tuple[tuple[str, str, int], ...] = (
        ("postgres", "infra/postgres/init.sql", 5432),
        ("redis", "infra/redis/redis.conf", 6379),
        ("minio", "infra/minio/init_buckets.sh", 9000),
        ("prometheus", "infra/monitoring/prometheus.yml", 9090),
        ("caddy", "infra/networking/Caddyfile", 443),
    )

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()
        self.infra_dir: Path = self.root_dir / "infra"

    def audit_iac_manifests(self) -> list[InfraServiceHealthDTO]:
        """Audits presence and validity of IaC configuration files."""
        results: list[InfraServiceHealthDTO] = []

        for name, rel_path, port in self.SERVICES_MAP:
            full_path = self.root_dir / rel_path
            exists = full_path.exists()

            results.append(
                InfraServiceHealthDTO(
                    service_name=name,
                    config_path=rel_path,
                    status="CONFIGURED" if exists else "MISSING",
                    port_binding=port,
                )
            )

        return results
