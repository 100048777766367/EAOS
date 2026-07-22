import uuid
from typing import Any

from packages.evolution.domain.governance import (
    CouncilVote,
    EvolutionGovernanceCouncil,
)
from packages.evolution.domain.models import (
    EvolutionObject,
    RollbackSnapshot,
    SemanticVersion,
    check_backwards_compatibility,
    migrate_payload,
)
from packages.evolution.domain.ports import EvolutionRepository


class ProposeEvolutionRequest:
    def __init__(
        self,
        id: str,
        name: str,
        payload: dict[str, Any],
        author: str,
        triggered_by: str,
        parent_id: str | None = None,
    ) -> None:
        self.id = id
        self.name = name
        self.payload = payload
        self.author = author
        self.triggered_by = triggered_by
        self.parent_id = parent_id


class ProposeEvolutionUseCase:
    def __init__(self, repo: EvolutionRepository, council: EvolutionGovernanceCouncil) -> None:
        self.repo = repo
        self.council = council

    def execute(self, request: ProposeEvolutionRequest, votes: list[CouncilVote]) -> EvolutionObject:
        from packages.evolution.domain.models import (
            Metadata,
            Provenance,
        )

        version_num = 1
        if request.parent_id:
            parent = self.repo.find_by_id(request.parent_id)
            if parent:
                comp, errs = check_backwards_compatibility(parent.payload, request.payload)
                if not comp:
                    raise ValueError(f"Evolution proposal violates compatibility: {errs}")
                version_num = parent.version.major + 1

        approved_count = sum(1 for v in votes if v.decision == "APPROVED")
        if approved_count < (len(votes) / 2):
            raise ValueError("Proposal rejected by Architecture Council.")

        new_payload = request.payload.copy()
        new_payload["__version"] = version_num

        meta = Metadata(environment="production", criticality="high")
        prov = Provenance(
            author=request.author,
            triggered_by=request.triggered_by,
            parent_id=request.parent_id,
        )

        sem_ver = SemanticVersion(major=version_num, minor=0, patch=0, revision="REV-AUTO")
        obj = EvolutionObject(
            id=request.id,
            name=request.name,
            version=sem_ver,
            payload=new_payload,
            metadata=meta,
            provenance=prov,
            evidences=[],
        )

        saved = self.repo.save(obj)
        self.council.evaluate_proposal(saved, votes)
        return saved


class MigrateEvolutionUseCase:
    def __init__(self, repo: EvolutionRepository) -> None:
        self.repo = repo

    def execute_migration(self, doc_id: str, rules: dict[str, Any], author: str) -> EvolutionObject:
        parent_obj = self.repo.find_by_id(doc_id)
        if not parent_obj:
            raise ValueError("Không tìm thấy tài liệu cha")

        snap_id = f"SNAP-{uuid.uuid4().hex[:6].upper()}"
        snapshot = RollbackSnapshot(
            snapshot_id=snap_id,
            target_id=doc_id,
            version_tag=parent_obj.version.to_string(),
            payload_backup=parent_obj.payload,
            original_payload=parent_obj.payload,
        )
        if hasattr(self.repo, "save_snapshot"):
            self.repo.save_snapshot(snapshot)

        new_payload = migrate_payload(parent_obj.payload, rules)
        new_version = parent_obj.version.major + 1
        new_payload["__version"] = new_version

        comp, errs = check_backwards_compatibility(parent_obj.payload, new_payload)
        if not comp:
            raise ValueError(f"Vi phạm tương thích ngược: {errs}")

        from packages.evolution.domain.models import (
            Evidence,
            Metadata,
            Provenance,
        )

        new_id = f"EVO-{uuid.uuid4().hex[:6].upper()}"
        meta = Metadata(environment="production", criticality="high")
        prov = Provenance(
            author=author,
            triggered_by="Automatic Migration",
            parent_id=doc_id,
        )
        ev = Evidence(
            metric_name="Backwards Compatibility",
            metric_value=1.0,
            passed=True,
            log_summary="Migration check passed",
        )
        sem_ver = SemanticVersion(major=new_version, minor=0, patch=0, revision="REV-MIG")
        obj = EvolutionObject(
            id=new_id,
            name=f"Migrated from {parent_obj.name}",
            version=sem_ver,
            payload=new_payload,
            metadata=meta,
            provenance=prov,
            evidences=[ev],
        )
        return self.repo.save(obj)

    def rollback(self, snapshot_id: str) -> EvolutionObject:
        snapshot = None
        if hasattr(self.repo, "find_snapshot_by_id"):
            snapshot = self.repo.find_snapshot_by_id(snapshot_id)
        elif hasattr(self.repo, "find_snapshot"):
            snapshot = self.repo.find_snapshot(snapshot_id)

        if not snapshot:
            raise ValueError(f"Snapshot {snapshot_id} không tồn tại")

        target = self.repo.find_by_id(snapshot.target_id)
        if not target:
            raise ValueError(f"Target {snapshot.target_id} không tồn tại")

        reverted_obj = EvolutionObject(
            id=target.id,
            name=target.name,
            version=target.version,
            payload=snapshot.original_payload or snapshot.payload_backup,
            metadata=target.metadata,
            provenance=target.provenance,
            evidences=target.evidences,
        )
        return self.repo.save(reverted_obj)
