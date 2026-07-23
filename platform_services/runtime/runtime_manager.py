"""Runtime manager and operational data inspector for EAOS."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict


class RuntimeStateSummaryDTO(BaseModel):
    """Value object representing the status of a runtime directory."""

    model_config = ConfigDict(frozen=True)

    directory_name: str
    file_count: int
    status: str


class RuntimeManagerEngine:
    """Engine auditing real-time operational data across 9 runtime domains."""

    SUBDIRECTORIES: tuple[str, ...] = (
        "cache",
        "events",
        "logs",
        "metrics",
        "policies",
        "registry",
        "sessions",
        "state",
        "traces",
    )

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()
        self.runtime_dir: Path = self.root_dir / "runtime"

    def inspect_runtime_health(self) -> list[RuntimeStateSummaryDTO]:
        """Audits all 9 runtime subdirectories and checks file states."""
        results: list[RuntimeStateSummaryDTO] = []
        if not self.runtime_dir.exists():
            return results

        for sub in self.SUBDIRECTORIES:
            sub_path = self.runtime_dir / sub
            file_count = 0
            is_active = False

            if sub_path.exists() and sub_path.is_dir():
                files = [f for f in sub_path.iterdir() if f.is_file() and not f.name.startswith(".")]
                file_count = len(files)
                is_active = True

            results.append(
                RuntimeStateSummaryDTO(
                    directory_name=sub,
                    file_count=file_count,
                    status="ACTIVE" if is_active else "UNINITIALIZED",
                )
            )

        return results
