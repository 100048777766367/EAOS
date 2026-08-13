from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

"""Validator auditing 58 Capability Packages for 7-file compliance."""


class CapabilityPackageStatusDTO(BaseModel):
    """Value object representing single Capability Package status."""

    model_config = ConfigDict(frozen=True)

    capability_id: str
    spec_files_count: int
    has_executable_code: bool
    is_fully_compliant: bool


class EnterpriseCapabilityPackageAuditor:
    """Auditor inspecting capability package completeness."""

    REQUIRED_FILES: ClassVar[tuple[str, ...]] = (
        "capability.md",
        "workflow.md",
        "domain.md",
        "api.yaml",
        "ui.md",
        "tasks.md",
        "tests.md",
    )

    def __init__(self, root_path: Path | str = ".") -> None:
        self.root_path = Path(root_path).resolve()

    def audit_all_packages(self) -> list[CapabilityPackageStatusDTO]:
        """Audits all directories under capabilities/."""
        cap_dir = self.root_path / "capabilities"
        pkg_dir = self.root_path / "packages"
        results: list[CapabilityPackageStatusDTO] = []

        if not cap_dir.exists():
            return results

        for c_folder in cap_dir.iterdir():
            if c_folder.is_dir() and not c_folder.name.startswith("."):
                c_id = c_folder.name
                file_count = sum(1 for rf in self.REQUIRED_FILES if (c_folder / rf).exists())
                code_exists = (pkg_dir / c_id / "domain" / "models.py").exists()

                results.append(
                    CapabilityPackageStatusDTO(
                        capability_id=c_id,
                        spec_files_count=file_count,
                        has_executable_code=code_exists,
                        is_fully_compliant=(file_count == 7),
                    )
                )

        return results


if __name__ == "__main__":
    auditor = EnterpriseCapabilityPackageAuditor()
    items = auditor.audit_all_packages()
    compliant_count = sum(1 for i in items if i.is_fully_compliant)
    executable_count = sum(1 for i in items if i.has_executable_code)
    print(
        f"✔ Capability Package Audit Complete: "
        f"{compliant_count}/{len(items)} Spec Compliant, "
        f"{executable_count} Fully Executable with Python Code."
    )
