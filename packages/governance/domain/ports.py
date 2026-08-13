from datetime import UTC, datetime
from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, Field

"""Domain Ports and DTOs for Governance Package."""


class ScanDiagnostic(BaseModel):
    """Mô tả chẩn đoán quét thành phần."""

    diagnostic_id: str = Field(default="")
    message: str = Field(default="")
    severity: str = Field(default="INFO")
    file_path: str = Field(default="")

    model_config = ConfigDict(frozen=True)


class AuditSnapshotDTO(BaseModel):
    """Mô tả ảnh chụp kiểm toán."""

    snapshot_id: str = Field(default="")
    status: str = Field(default="COMMITTED")
    audit_status: str = Field(default="PASSED")
    active_source_files: int = Field(default=0)
    empty_directories: int = Field(default=0)
    architecture_violations: int = Field(default=0)
    audit_warnings_count: int = Field(default=0)
    calculated_health_score: float = Field(default=100.0)
    coupling_index: float = Field(default=0.0)
    instability_index: float = Field(default=0.0)
    package_cohesion: float = Field(default=1.0)
    diagnostics_summary: list[Any] = Field(default_factory=list)
    timestamp: datetime | float = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class TopologyScanDTO(BaseModel):
    """Mô tả kết quả quét địa hình kiến trúc."""

    scan_id: str = Field(default="")
    nodes_count: int = Field(default=0)
    active_py_files: int = Field(default=0)
    empty_directories: int = Field(default=0)
    import_records: list[Any] = Field(default_factory=list)
    diagnostics: list[ScanDiagnostic] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class TopologyScannerPort(Protocol):
    """Port for scanning component topology."""

    def scan_topology(self) -> TopologyScanDTO: ...

    def scan_workspace(self) -> TopologyScanDTO: ...


class GovernancePolicyProviderPort(Protocol):
    """Port for providing governance policies."""

    def get_policies(self) -> list[dict[str, Any]]: ...

    def load_policy(self) -> Any: ...


class GovernanceRepositoryPort(Protocol):
    """Port for governance persistence."""

    def save_snapshot(self, snapshot: AuditSnapshotDTO) -> None: ...

    def get_latest_snapshot(self) -> AuditSnapshotDTO | None: ...

    def count_records(self) -> int: ...


class KnowledgeGraphPort(Protocol):
    """Port for knowledge graph interaction."""

    def query_graph(self, query: str) -> dict[str, Any]: ...

    def query_system_node_count(self) -> int: ...


__all__ = [
    "AuditSnapshotDTO",
    "GovernancePolicyProviderPort",
    "GovernanceRepositoryPort",
    "KnowledgeGraphPort",
    "ScanDiagnostic",
    "TopologyScanDTO",
    "TopologyScannerPort",
]
