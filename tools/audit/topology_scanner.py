"""Enterprise Architecture Topology Scanner & Asset Discovery Engine."""

import json
from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class DirectoryAuditEntryDTO(BaseModel):
    """Value object representing physical state of a root directory."""

    model_config = ConfigDict(frozen=True)

    name: str
    status: str
    file_count: int
    total_size_bytes: int


class TopologyScanReportDTO(BaseModel):
    """Value object containing comprehensive workspace audit report."""

    model_config = ConfigDict(frozen=True)

    canonical_layers_found: int
    canonical_layers_missing: int
    unindexed_assets_found: int
    total_files_scanned: int
    empty_directories_count: int
    extension_matrix: dict[str, int]
    details: list[DirectoryAuditEntryDTO]


class MonorepoTopologyScanner:
    """Scanner comparing disk structure against canonical EA manifest."""

    CANONICAL_ROOTS: ClassVar[tuple[str, ...]] = (
        ".agents",
        ".github",
        "agents",
        "ai",
        "apps",
        "architecture",
        "assets",
        "capabilities",
        "catalog",
        "configs",
        "contexts",
        "contracts",
        "data",
        "decision",
        "digital_twin",
        "docs",
        "ecosystem",
        "engine",
        "evolution",
        "examples",
        "extensions",
        "federation",
        "fitness",
        "generated",
        "infra",
        "kernel",
        "knowledge",
        "libs",
        "marketplace",
        "memory",
        "meta",
        "operating_model",
        "operations",
        "observability",
        "packages",
        "platform",
        "platform_layer",
        "platform_services",
        "policies",
        "portfolio",
        "products",
        "rules",
        "runtime",
        "schemas",
        "scripts",
        "sdk",
        "security",
        "services",
        "specifications",
        "tests",
        "tools",
        "views",
    )

    IGNORED_DIRS: ClassVar[set[str]] = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "build",
        "dist",
        ".idea",
        ".vscode",
    }

    def __init__(self, root_path: Path | str = ".") -> None:
        self.root_path = Path(root_path).resolve()

    def clean_empty_directories(self) -> int:
        """Finds and populates hollow empty directories with __init__.py."""
        cleaned = 0
        for d in self.root_path.rglob("*"):
            if d.is_dir() and not any(p in self.IGNORED_DIRS for p in d.parts) and not any(d.iterdir()):
                init_file = d / "__init__.py"
                init_file.write_text('"""Module initializer."""\n', encoding="utf-8")
                cleaned += 1
        return cleaned

    def scan_workspace(self) -> TopologyScanReportDTO:
        """Performs full workspace audit and discovers unindexed assets."""
        self.clean_empty_directories()

        found_canonical = 0
        missing_canonical = 0
        unindexed_count = 0
        details: list[DirectoryAuditEntryDTO] = []
        ext_matrix: dict[str, int] = {}
        empty_dirs = 0

        for canonical in self.CANONICAL_ROOTS:
            p = self.root_path / canonical
            if p.exists() and p.is_dir():
                found_canonical += 1
                files = [f for f in p.rglob("*") if f.is_file()]
                size = sum(f.stat().st_size for f in files if f.exists())
                details.append(
                    DirectoryAuditEntryDTO(
                        name=canonical,
                        status="EXISTS",
                        file_count=len(files),
                        total_size_bytes=size,
                    )
                )
            else:
                missing_canonical += 1
                details.append(
                    DirectoryAuditEntryDTO(
                        name=canonical,
                        status="MISSING",
                        file_count=0,
                        total_size_bytes=0,
                    )
                )

        for item in self.root_path.iterdir():
            if item.is_dir() and item.name not in self.CANONICAL_ROOTS and item.name not in self.IGNORED_DIRS:
                unindexed_count += 1
                files = [f for f in item.rglob("*") if f.is_file()]
                size = sum(f.stat().st_size for f in files if f.exists())
                details.append(
                    DirectoryAuditEntryDTO(
                        name=item.name,
                        status="DISCOVERED_UNINDEXED",
                        file_count=len(files),
                        total_size_bytes=size,
                    )
                )

        total_files = 0
        for f in self.root_path.rglob("*"):
            if f.is_file() and not any(part in self.IGNORED_DIRS for part in f.parts):
                total_files += 1
                ext = f.suffix.lower() or "[no_ext]"
                ext_matrix[ext] = ext_matrix.get(ext, 0) + 1

        for d in self.root_path.rglob("*"):
            if d.is_dir() and not any(part in self.IGNORED_DIRS for part in d.parts) and not any(d.iterdir()):
                empty_dirs += 1

        report = TopologyScanReportDTO(
            canonical_layers_found=found_canonical,
            canonical_layers_missing=missing_canonical,
            unindexed_assets_found=unindexed_count,
            total_files_scanned=total_files,
            empty_directories_count=empty_dirs,
            extension_matrix=ext_matrix,
            details=details,
        )

        manifest_dir = self.root_path / "runtime" / "inventory"
        manifest_dir.mkdir(parents=True, exist_ok=True)
        manifest_file = manifest_dir / "discovered_assets_manifest.json"
        manifest_file.write_text(
            json.dumps(report.model_dump(), indent=2),
            encoding="utf-8",
        )

        return report


if __name__ == "__main__":
    scanner = MonorepoTopologyScanner()
    rep = scanner.scan_workspace()
    print(f"✔ Scan Complete! Total files scanned: {rep.total_files_scanned}")
