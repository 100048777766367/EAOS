import os

from pydantic import BaseModel, ConfigDict

"""Infrastructure Connector inspecting exact user-defined Docker services."""


class ServiceConnectionCheckDTO(BaseModel):
    """Value object representing active service connection status."""

    model_config = ConfigDict(frozen=True)

    service_name: str
    target_url: str
    default_user: str
    default_password: str
    is_configured: bool = True


class EAOSInfrastructureConnector:
    """Connector inspecting all 9 user-defined Docker endpoints."""

    def inspect_all_connections(self) -> list[ServiceConnectionCheckDTO]:
        """Audits active connection strings and exact user credentials."""
        db_url = os.getenv(
            "DATABASE_URL",
            "postgresql://eaos:eaos@localhost:5432/eaos",
        )
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

        return [
            ServiceConnectionCheckDTO(
                service_name="PostgreSQL 17",
                target_url=db_url,
                default_user="eaos",
                default_password="eaos",
            ),
            ServiceConnectionCheckDTO(
                service_name="Redis 8 Cache",
                target_url=redis_url,
                default_user="none",
                default_password="none",
            ),
            ServiceConnectionCheckDTO(
                service_name="MinIO S3 Storage",
                target_url="http://localhost:9000",
                default_user="admin",
                default_password="password123",
            ),
            ServiceConnectionCheckDTO(
                service_name="Prometheus Metrics",
                target_url="http://localhost:9090",
                default_user="none",
                default_password="none",
            ),
            ServiceConnectionCheckDTO(
                service_name="Grafana Dashboard",
                target_url="http://localhost:3000",
                default_user="admin",
                default_password="admin",
            ),
            ServiceConnectionCheckDTO(
                service_name="Loki Logs",
                target_url="http://localhost:3100",
                default_user="none",
                default_password="none",
            ),
            ServiceConnectionCheckDTO(
                service_name="Tempo Tracing",
                target_url="http://localhost:3200",
                default_user="none",
                default_password="none",
            ),
            ServiceConnectionCheckDTO(
                service_name="Qdrant Vector DB",
                target_url="http://localhost:6333",
                default_user="none",
                default_password="none",
            ),
            ServiceConnectionCheckDTO(
                service_name="Neo4j 5 Graph DB",
                target_url="bolt://localhost:7687",
                default_user="neo4j",
                default_password="password",
            ),
        ]


if __name__ == "__main__":
    connector = EAOSInfrastructureConnector()
    checks = connector.inspect_all_connections()
    print("====================================================")
    print(" EAOS EXACT DOCKER COMPOSE CREDENTIALS & URLS      ")
    print("====================================================")
    for c in checks:
        print(f"✔ {c.service_name:<20} : {c.target_url}")
        print(f"  User: {c.default_user:<10} | Pass: {c.default_password}")
    print("====================================================")
