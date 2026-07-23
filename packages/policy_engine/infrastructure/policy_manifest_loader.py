"""Infrastructure adapter loading declarative Policy-as-Code YAML manifests."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict


class PolicyManifestDTO(BaseModel):
    """Value object representing a declarative Policy-as-Code manifest."""

    model_config = ConfigDict(frozen=True)

    policy_id: str
    category: str
    version: str
    file_path: str


class PolicyManifestLoader:
    """Loader discovering and validating policy manifests across 7 categories."""

    CATEGORIES: tuple[str, ...] = (
        "ai",
        "architecture",
        "compliance",
        "engineering",
        "governance",
        "quality",
        "security",
    )

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()
        self.policies_dir: Path = self.root_dir / "policies"

    def discover_policies(self) -> list[PolicyManifestDTO]:
        """Scans all policy subdirectories for declarative YAML files."""
        results: list[PolicyManifestDTO] = []
        if not self.policies_dir.exists():
            return results

        for cat in self.CATEGORIES:
            cat_dir = self.policies_dir / cat
            if cat_dir.exists() and cat_dir.is_dir():
                results.extend(
                    PolicyManifestDTO(
                        policy_id=item.stem,
                        category=cat,
                        version="1.0.0",
                        file_path=str(item.relative_to(self.root_dir)),
                    )
                    for item in cat_dir.iterdir()
                    if (item.is_file() and item.suffix in (".yaml", ".yml") and not item.name.startswith("."))
                )

        return results
