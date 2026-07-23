"""Boilerplate code synthesizer generating Hexagonal DDD package structures."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict


class GeneratedBoilerplateDTO(BaseModel):
    """Value object representing generated package boilerplate details."""

    model_config = ConfigDict(frozen=True)

    package_name: str
    created_files: list[str]
    status: str


class BoilerplateGeneratorTool:
    """Tool generating hexagonal package scaffolding (domain, application, infra)."""

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()

    def generate_package(
        self,
        package_name: str,
    ) -> GeneratedBoilerplateDTO:
        """Generates domain, application, and infra folders for a package."""
        base_dir = self.root_dir / "packages" / package_name
        created: list[str] = []

        for sub in ("domain", "application", "infrastructure"):
            sub_dir = base_dir / sub
            sub_dir.mkdir(parents=True, exist_ok=True)
            init_file = sub_dir / "__init__.py"
            if not init_file.exists():
                init_file.write_text('""\n', encoding="utf-8")
            created.append(str(sub_dir.relative_to(self.root_dir)))

        return GeneratedBoilerplateDTO(
            package_name=package_name,
            created_files=created,
            status="GENERATED",
        )
