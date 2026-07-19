import uuid
from typing import Any

from pydantic import BaseModel

from packages.evolution.domain.governance import (
    CouncilVote,
    EvolutionGovernanceCouncil,
)
from packages.evolution.domain.models import (
    Evidence,
    EvolutionObject,
    Metadata,
    Provenance,
    RollbackSnapshot,
    SemanticVersion,
    check_backwards_compatibility,
    migrate_payload,
)
from packages.evolution.domain.ports import EvolutionRepository
from packages.evolution.domain.rules_engine import (
    CriticalityEnvironmentRule,
    PolicyEngine,
    VersionHeaderRule,
)


class ProposeEvolutionRequest(BaseModel):
    id: str
    name: str
    payload: dict[str, Any]
    author: str
    triggered_by: str
    parent_id: str | None = None
    environment: str = "production"
    criticality: str = "high"


class ProposeEvolutionUseCase:
    """Application Service điều phối Tiến hóa bắt buộc qua Governance."""

    def __init__(
        self,
        repo: EvolutionRepository,
        council: EvolutionGovernanceCouncil,
    ) -> None:
        self.repo = repo
        self.council = council

    def execute(
        self,
        request: ProposeEvolutionRequest,
        votes: list[CouncilVote],
    ) -> EvolutionObject:
        # 1. Khởi tạo phiên bản bất biến (Immutable Version)
        rev = uuid.uuid4().hex[:8].upper()
        major, minor, patch = 1, 0, 0

        if request.parent_id:
            parent_obj = self.repo.find_by_id(request.parent_id)
            if parent_obj:
                major = parent_obj.version.major
                minor = parent_obj.version.minor + 1
                patch = parent_obj.version.patch

        version = SemanticVersion(major=major, minor=minor, patch=patch, revision=rev)

        metadata = Metadata(
            environment=request.environment,
            criticality=request.criticality,
        )
        provenance = Provenance(
            author=request.author,
            triggered_by=request.triggered_by,
            parent_id=request.parent_id,
        )

        # Tạo đối tượng tạm thời để thẩm định Policy & Fitness
        temp_obj = EvolutionObject(
            id=request.id,
            name=request.name,
            version=version,
            payload=request.payload,
            metadata=metadata,
            provenance=provenance,
            evidences=[],
        )

        # 2. KIỂM TOÁN POLICY (Policy Engine)
        policy = PolicyEngine(
            name="Evolution Governance Policy",
            rules=[VersionHeaderRule(), CriticalityEnvironmentRule()],
        )
        passed, _ = policy.evaluate_policy(temp_obj)

        if not passed:
            raise ValueError("Proposal bị từ chối do vi phạm Policy Engine hiến pháp.")

        # 3. BIỂU QUYẾT HỘI ĐỒNG (Architecture Council Voting)
        tx = self.council.evaluate_proposal(temp_obj, votes)
        if tx.status != "APPROVED":
            raise ValueError("Proposal bị Hội đồng Kiến trúc (Council) bác bỏ.")

        # 4. COMMIT & LƯU VẾT
        evidence = Evidence(
            metric_name="Governance Consensus Check",
            metric_value=1.0,
            passed=True,
            log_summary=f"Phê duyệt thành công qua giao dịch {tx.tx_id}",
        )

        committed_obj = EvolutionObject(
            id=request.id,
            name=request.name,
            version=version,
            payload=request.payload,
            metadata=metadata,
            provenance=provenance,
            evidences=[evidence],
        )

        return self.repo.save(committed_obj)


class MigrateEvolutionUseCase:
    """Application Service di chuyển dữ liệu có Snapshot & Rollback tự động."""

    def __init__(self, repo: EvolutionRepository) -> None:
        self.repo = repo

    def execute_migration(
        self,
        doc_id: str,
        migration_rules: dict[str, Any],
        author: str,
    ) -> EvolutionObject:
        parent_obj = self.repo.find_by_id(doc_id)
        if not parent_obj:
            raise ValueError(f"Không tìm thấy đối tượng gốc: {doc_id}")

        # 1. PRE-MIGRATION SNAPSHOT (Tạo bản sao lưu trữ để phục hồi)
        snap_id = f"SNAP-{uuid.uuid4().hex[:6].upper()}"
        snapshot = RollbackSnapshot(
            snapshot_id=snap_id,
            target_id=doc_id,
            original_payload=parent_obj.payload,
        )
        self.repo.save_snapshot(snapshot)

        # 2. MIGRATION (Áp dụng quy tắc biến đổi)
        new_payload = migrate_payload(parent_obj.payload, migration_rules)

        # 3. VALIDATION (Kiểm tra tương thích ngược)
        compatible, errors = check_backwards_compatibility(
            parent_obj.payload, new_payload
        )

        # 4. ROLLBACK (Nếu kiểm định thất bại, tự động hoàn tác về Snapshot)
        if not compatible:
            self.rollback(snap_id)
            raise ValueError(
                f"Vi phạm tương thích ngược. Đã Rollback về Snapshot {snap_id}: "
                f"{', '.join(errors)}"
            )

        # 5. COMMIT (Tạo nút phiên bản bất biến mới)
        new_id = f"EVO-{uuid.uuid4().hex[:6].upper()}"
        new_version = SemanticVersion(
            major=parent_obj.version.major,
            minor=parent_obj.version.minor + 1,
            patch=parent_obj.version.patch,
            revision=uuid.uuid4().hex[:8].upper(),
        )

        meta = Metadata(environment="production", criticality="high")
        prov = Provenance(
            author=author,
            triggered_by="Migration with Rollback Guard",
            parent_id=doc_id,
        )
        evidence = Evidence(
            metric_name="Migration Compatibility Check",
            metric_value=1.0,
            passed=True,
            log_summary=f"Migration thành công từ Snapshot {snap_id}",
        )

        new_obj = EvolutionObject(
            id=new_id,
            name=f"Migrated {parent_obj.name}",
            version=new_version,
            payload=new_payload,
            metadata=meta,
            provenance=prov,
            evidences=[evidence],
        )

        return self.repo.save(new_obj)

    def rollback(self, snapshot_id: str) -> EvolutionObject:
        """Thực thi hoàn tác (Rollback) khôi phục về trạng thái Snapshot."""
        snapshot = self.repo.find_snapshot(snapshot_id)
        if not snapshot:
            raise ValueError(f"Không tìm thấy Snapshot hoàn tác: {snapshot_id}")

        target_obj = self.repo.find_by_id(snapshot.target_id)
        if not target_obj:
            raise ValueError("Không tìm thấy đối tượng cần hoàn tác.")

        rolled_back_version = SemanticVersion(
            major=target_obj.version.major,
            minor=target_obj.version.minor,
            patch=target_obj.version.patch + 1,
            revision=f"ROLLBACK-{uuid.uuid4().hex[:4].upper()}",
        )

        evidence = Evidence(
            metric_name="Rollback Execution",
            metric_value=1.0,
            passed=True,
            log_summary=f"Khôi phục hoàn hảo từ Snapshot {snapshot_id}",
        )

        reverted_obj = EvolutionObject(
            id=target_obj.id,
            name=f"Reverted {target_obj.name}",
            version=rolled_back_version,
            payload=snapshot.original_payload,
            metadata=target_obj.metadata,
            provenance=target_obj.provenance,
            evidences=[evidence],
        )

        return self.repo.save(reverted_obj)
