import urllib.request
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

"""Endpoint Inspector probing live health of all 9 EAOS services."""


class EndpointStatusDTO(BaseModel):
    """Value object representing single endpoint probe status."""

    model_config = ConfigDict(frozen=True)

    service_name: str
    url: str
    is_online: bool
    status_code: int


class EAOSEndpointInspector:
    """Probes live HTTP connectivity across all EAOS Control Dashboards."""

    ENDPOINTS: ClassVar[dict[str, str]] = {
        "API Gateway": "http://127.0.0.1:8000/health",
        "Control Room UI": "http://127.0.0.1:8000/dashboard",
        "Prometheus UI": "http://127.0.0.1:9090",
        "Grafana UI": "http://127.0.0.1:3000",
        "MinIO API": "http://127.0.0.1:9000/minio/health/live",
        "Qdrant Vector DB": "http://127.0.0.1:6333/healthz",
        "Loki Log Engine": "http://127.0.0.1:3100/ready",
        "Tempo Tracing": "http://127.0.0.1:3200",
        "Neo4j HTTP Console": "http://127.0.0.1:7474",
    }

    def probe_all_endpoints(self) -> list[EndpointStatusDTO]:
        """Executes HTTP probe calls across all 9 control endpoints."""
        results: list[EndpointStatusDTO] = []
        for name, url in self.ENDPOINTS.items():
            is_ok = False
            code = 0
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "EAOS-Inspector/1.0"})
                with urllib.request.urlopen(req, timeout=2) as resp:
                    code = resp.getcode()
                    is_ok = code < 500
            except Exception:
                is_ok = False
                code = 0

            results.append(
                EndpointStatusDTO(
                    service_name=name,
                    url=url,
                    is_online=is_ok,
                    status_code=code,
                )
            )

        return results


if __name__ == "__main__":
    inspector = EAOSEndpointInspector()
    probes = inspector.probe_all_endpoints()
    print("✔ EAOS 9-Endpoint Health Probe Completed:")
    for p in probes:
        status_str = "ONLINE" if p.is_online else "OFFLINE (Start Docker)"
        print(f"  - {p.service_name:<20} [{p.url}] : {status_str}")
