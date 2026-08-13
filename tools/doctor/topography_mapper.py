from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import ClassVar  # Import ClassVar

"""EAOS Topography Mapper & Architectural Ring Auditor."""


class ArchitectureRing(Enum):
    """Phân cấp 4 Vòng đai Kiến trúc EAOS."""

    RING_0_KERNEL = "RING_0_KERNEL"
    RING_1_BUSINESS = "RING_1_BUSINESS"
    RING_2_DELIVERY = "RING_2_DELIVERY"
    RING_3_GOVERNANCE = "RING_3_GOVERNANCE"
    TEMPORARY_CACHE = "TEMPORARY_CACHE"


@dataclass(frozen=True, slots=True)
class TopographyDirectoryInfo:
    """Thông tin phân loại thư mục."""

    name: str
    ring: ArchitectureRing
    description: str


class EAOSTopographyAuditor:
    """Công cụ kiểm toán cấu trúc Monorepo dựa trên hình ảnh thực tế."""

    # Khai báo ClassVar sửa lỗi RUF012
    RING_MAPPING: ClassVar[dict[str, ArchitectureRing]] = {
        ".venv": ArchitectureRing.TEMPORARY_CACHE,
        "venvss": ArchitectureRing.TEMPORARY_CACHE,
        ".mypy_cache": ArchitectureRing.TEMPORARY_CACHE,
        ".pytest_cache": ArchitectureRing.TEMPORARY_CACHE,
        ".pytest_tmp": ArchitectureRing.TEMPORARY_CACHE,
        ".ruff_cache": ArchitectureRing.TEMPORARY_CACHE,
        ".eaos_backups": ArchitectureRing.TEMPORARY_CACHE,
        "__pycache__": ArchitectureRing.TEMPORARY_CACHE,
        "kernel": ArchitectureRing.RING_0_KERNEL,
        "engine": ArchitectureRing.RING_0_KERNEL,
        "packages": ArchitectureRing.RING_1_BUSINESS,
        "capabilities": ArchitectureRing.RING_1_BUSINESS,
        "memory": ArchitectureRing.RING_1_BUSINESS,
        "knowledge": ArchitectureRing.RING_1_BUSINESS,
        "apps": ArchitectureRing.RING_2_DELIVERY,
        "docs": ArchitectureRing.RING_3_GOVERNANCE,
        "policies": ArchitectureRing.RING_3_GOVERNANCE,
        "rules": ArchitectureRing.RING_3_GOVERNANCE,
        "contracts": ArchitectureRing.RING_3_GOVERNANCE,
        "infra": ArchitectureRing.RING_3_GOVERNANCE,
        "tools": ArchitectureRing.RING_3_GOVERNANCE,
        "tests": ArchitectureRing.RING_3_GOVERNANCE,
    }

    def audit_workspace_root(self, root_path: Path) -> list[TopographyDirectoryInfo]:
        """Phân loại toàn bộ các thư mục tại gốc D:\\EAOS."""
        results: list[TopographyDirectoryInfo] = []
        for item in root_path.iterdir():
            if item.is_dir():
                ring = self.RING_MAPPING.get(item.name, ArchitectureRing.RING_3_GOVERNANCE)
                results.append(
                    TopographyDirectoryInfo(
                        name=item.name,
                        ring=ring,
                        description=f"Thư mục {item.name} thuộc {ring.value}",
                    )
                )
        return results
