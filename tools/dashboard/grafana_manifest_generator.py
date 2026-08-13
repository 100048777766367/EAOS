import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict

"""Grafana Community Dashboard Manifest Generator for EAOS Observability."""


class GrafanaDashboardPanelDTO(BaseModel):
    """Value object representing a Grafana dashboard panel definition."""

    model_config = ConfigDict(frozen=True)

    panel_id: int
    title: str
    panel_type: str
    promql_query: str


class EAOSGrafanaManifestGenerator:
    """Engine generating native Grafana Community dashboard JSON specs."""

    def __init__(self, root_path: Path | str = ".") -> None:
        self.root_path = Path(root_path).resolve()

    def generate_grafana_json(self) -> Path:
        """Generates importable Grafana Community JSON Dashboard manifest."""
        obs_dir = self.root_path / "observability"
        obs_dir.mkdir(parents=True, exist_ok=True)
        dash_path = obs_dir / "grafana_dashboard.json"

        manifest = {
            "title": "EAOS Cybernetic Control Room Dashboard",
            "tags": ["eaos", "observability", "architecture"],
            "timezone": "browser",
            "schemaVersion": 36,
            "panels": [
                {
                    "id": 1,
                    "title": "Architectural Health Score",
                    "type": "gauge",
                    "targets": [{"expr": "eaos_architecture_health_score"}],
                },
                {
                    "id": 2,
                    "title": "API P99 Latency (ms)",
                    "type": "timeseries",
                    "targets": [{"expr": "eaos_api_p99_latency_ms"}],
                },
                {
                    "id": 3,
                    "title": "Architectural Drift Index",
                    "type": "stat",
                    "targets": [{"expr": "eaos_architecture_drift_index"}],
                },
            ],
        }

        dash_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return dash_path


if __name__ == "__main__":
    gen = EAOSGrafanaManifestGenerator()
    out = gen.generate_grafana_json()
    print(f"✔ Grafana Dashboard Manifest Generated: {out}")
