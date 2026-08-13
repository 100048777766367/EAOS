from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

"""Monorepo Package Registry and Governance Audit Engine."""


class MonorepoPackageSpecDTO(BaseModel):
    """Value object representing a monorepo package audit snapshot."""

    model_config = ConfigDict(frozen=True)

    package_name: str = Field(..., description="Package name e.g. agent")
    has_readme: bool = Field(default=True)
    has_init: bool = Field(default=True)
    subfolders_count: int = Field(default=0)
    is_compliant: bool = Field(default=True)


class MonorepoPackageRegistryEngine:
    """Engine auditing all 58+ domain packages in packages/."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()
        self.pkg_dir = self.root / "packages"

    def audit_all_packages(self) -> list[MonorepoPackageSpecDTO]:
        """Scan and audit all monorepo packages for governance."""
        if not self.pkg_dir.exists():
            return []

        specs: list[MonorepoPackageSpecDTO] = []
        for p in sorted(self.pkg_dir.iterdir()):
            if not p.is_dir() or p.name.startswith((".", "__")):
                continue

            has_readme = (p / "README.md").exists()
            has_init = (p / "__init__.py").exists()

            sub_dirs = [d for d in p.rglob("*") if d.is_dir() and "__" not in d.name]
            missing_inits = [d for d in sub_dirs if not (d / "__init__.py").exists()]

            compliant = has_readme and has_init and len(missing_inits) == 0

            specs.append(
                MonorepoPackageSpecDTO(
                    package_name=p.name,
                    has_readme=has_readme,
                    has_init=has_init,
                    subfolders_count=len(sub_dirs),
                    is_compliant=compliant,
                )
            )

        return specs
