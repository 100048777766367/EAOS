"""Infrastructure adapter for scanning and loading Business Capability YAMLs."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict


class CapabilityManifestDTO(BaseModel):
    """Value object representing a Business Capability manifest."""

    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    domain: str
    status: str
    version: str
    owner: str
    bounded_context: str


class CapabilityCatalogLoader:
    """Catalog loader reading YAML capability manifests across the enterprise."""

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()
        self.catalog_dir: Path = self.root_dir / "capabilities"

    def scan_catalog(self) -> list[CapabilityManifestDTO]:
        """Scans capability catalog directory for valid capability.yaml files."""
        results: list[CapabilityManifestDTO] = []
        if not self.catalog_dir.exists():
            return results

        for cap_dir in self.catalog_dir.iterdir():
            if cap_dir.is_dir() and not cap_dir.name.startswith("."):
                yaml_file = cap_dir / "capability.yaml"
                if yaml_file.exists():
                    manifest = self._parse_manifest_simple(yaml_file, cap_dir.name)
                    results.append(manifest)

        return results

    def _parse_manifest_simple(
        self,
        file_path: Path,
        dir_name: str,
    ) -> CapabilityManifestDTO:
        """Parses capability.yaml line-by-line without external dependencies."""
        lines = file_path.read_text(encoding="utf-8").splitlines()
        data: dict[str, str] = {}

        for line in lines:
            stripped = line.strip()
            if stripped and ":" in stripped and not stripped.startswith("#"):
                parts = stripped.split(":", 1)
                key = parts[0].strip()
                val = parts[1].strip().strip('"').strip("'")
                data[key] = val

        return CapabilityManifestDTO(
            id=data.get("id", f"cap.{dir_name}"),
            name=data.get("name", f"{dir_name.capitalize()} Capability"),
            domain=data.get("domain", dir_name.capitalize()),
            status=data.get("status", "ACTIVE"),
            version=data.get("version", "1.0.0"),
            owner=data.get("owner", "Chief Enterprise Architect"),
            bounded_context=data.get("bounded_context", f"packages/{dir_name}"),
        )
