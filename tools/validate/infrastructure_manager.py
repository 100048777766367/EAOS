from __future__ import annotations

import shutil
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

"""Infrastructure-as-Code (IaC) & Deployment Manager Engine."""


class IaCManifestDTO(BaseModel):
    """Value object representing an Infrastructure-as-Code manifest."""

    model_config = ConfigDict(frozen=True)

    manifest_id: str = Field(..., description="Manifest ID e.g. docker")
    category: str = Field(..., description="COMPOSE, HELM, K8S, TERRAFORM")
    file_path: str = Field(..., description="Relative file path")
    is_present: bool = Field(default=True)


class InfrastructureManagerEngine:
    """Engine auditing IaC manifests across Helm, K8s, Docker & Terraform."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()
        self.infra_dir = self.root / "infra"

    def audit_iac_manifests(self) -> list[IaCManifestDTO]:
        """Audit presence of essential Infrastructure-as-Code files."""
        if not self.infra_dir.exists():
            return []

        manifests = [
            ("docker-compose", "COMPOSE", "infra/compose/docker-compose.yml"),
            ("dockerfile-api", "DOCKER", "infra/docker/Dockerfile.api"),
            ("helm-chart", "HELM", "infra/helm/eaos/Chart.yaml"),
            ("k8s-deployment", "K8S", "infra/k8s/deployment.yaml"),
            ("terraform-main", "TERRAFORM", "infra/terraform/main.tf"),
            ("caddyfile", "NETWORKING", "infra/networking/Caddyfile"),
            ("postgres-init", "DATABASE", "infra/postgres/init.sql"),
        ]

        results: list[IaCManifestDTO] = []
        for m_id, cat, rel_path in manifests:
            fpath = self.root / rel_path
            results.append(
                IaCManifestDTO(
                    manifest_id=m_id,
                    category=cat,
                    file_path=rel_path,
                    is_present=fpath.exists(),
                )
            )

        return results

    def purge_misplaced_and_inits(self) -> int:
        """Remove misplaced packages/tests & invalid __init__.py in infra."""
        if not self.infra_dir.exists():
            return 0

        purged = 0

        for misplaced_name in ["packages", "tests"]:
            target_dir = self.infra_dir / "compose" / misplaced_name
            if target_dir.exists():
                shutil.rmtree(target_dir, ignore_errors=True)
                purged += 1

        for init_file in self.infra_dir.rglob("__init__.py"):
            try:
                init_file.unlink()
                purged += 1
            except Exception:
                pass

        return purged
