"""Consistency verifier inspecting capability line-of-sight mapping."""

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict


class ConsistencyReportDTO(BaseModel):
    """Value object representing consistency audit results."""

    model_config = ConfigDict(frozen=True)

    total_packages: int
    mapped_capabilities: int
    unmapped_packages: list[str]
    consistency_score: float
    is_consistent: bool


class ConsistencyVerifier:
    """Verifier ensuring 100% of packages map to Business Capabilities."""

    def __init__(self, root_path: Path | str = ".") -> None:
        self.root_path = Path(root_path).resolve()

    def verify_consistency(self) -> ConsistencyReportDTO:
        """Verifies packages against capability traceability matrix."""
        matrix_path = self.root_path / "knowledge" / "traceability" / "capability_traceability_matrix.json"
        mapped_packages: set[str] = set()

        if matrix_path.exists():
            try:
                data = json.loads(matrix_path.read_text(encoding="utf-8"))
                for entry in data.get("capability_mappings", []):
                    pkg = entry.get("package", "").replace("packages/", "")
                    if pkg:
                        mapped_packages.add(pkg)
            except Exception:
                pass

        pkg_dir = self.root_path / "packages"
        unmapped: list[str] = []
        total_pkgs = 0

        if pkg_dir.exists():
            for p in pkg_dir.iterdir():
                if p.is_dir() and p.name not in {
                    "__pycache__",
                    "shared",
                }:
                    total_pkgs += 1
                    if p.name not in mapped_packages:
                        unmapped.append(p.name)

        mapped_count = total_pkgs - len(unmapped)
        score = (mapped_count / total_pkgs * 100.0) if total_pkgs else 100.0

        return ConsistencyReportDTO(
            total_packages=total_pkgs,
            mapped_capabilities=mapped_count,
            unmapped_packages=unmapped,
            consistency_score=round(score, 2),
            is_consistent=len(unmapped) == 0,
        )


if __name__ == "__main__":
    verifier = ConsistencyVerifier()
    rep = verifier.verify_consistency()
    print(f"✔ Consistency Verification Score: {rep.consistency_score}%")
