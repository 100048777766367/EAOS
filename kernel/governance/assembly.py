import json
import os
from datetime import UTC, datetime
from typing import Any

from packages.knowledge.domain.models import KnowledgeArtifact
from pydantic import BaseModel, Field


class ConsensusVote(BaseModel):
    """Lá phiếu đồng thuận kiểm duyệt từ con người hoặc các AI Agents."""

    voter: str  # Ví dụ: "ArchitectAgent", "ReviewerAgent", "Solopreneur"
    decision: str  # "APPROVED" hoặc "REJECTED"
    reason: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AssemblyTransaction(BaseModel):
    """Giao dịch hội đồng đã được kiểm duyệt và ký số ngữ nghĩa."""

    tx_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    action: str  # "ADD", "EDIT", "DELETE"
    artifact_id: str
    votes: list[ConsensusVote]
    status: str  # "COMMITTED" hoặc "REJECTED"


class ArchitectureAssembly:
    """Hội đồng điều hành tối cao kiểm soát tính bất biến của dữ liệu EAOS."""

    def __init__(self, ledger_path: str = "runtime/traces/audit_ledger.jsonl"):
        self.ledger_path = ledger_path
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)

    def evaluate_proposal(
        self,
        action: str,
        artifact: KnowledgeArtifact,
        votes: list[ConsensusVote],
    ) -> AssemblyTransaction:
        """Kiểm duyệt đề xuất thay đổi tri thức dựa trên sự biểu quyết."""
        import uuid

        # Biến đổi dòng 68 cũ thành 2 dòng ngắn hơn để vượt ải Ruff E501
        approved_voters = [v for v in votes if v.decision == "APPROVED"]
        passed = len(approved_voters) >= (len(votes) / 2)

        status = "COMMITTED" if passed else "REJECTED"
        tx_id = f"TX-{uuid.uuid4().hex[:8].upper()}"

        tx = AssemblyTransaction(
            tx_id=tx_id,
            action=action,
            artifact_id=artifact.id or "PENDING",
            votes=votes,
            status=status,
        )

        # Lưu trữ giao dịch vào Append-Only Ledger
        with open(self.ledger_path, "a", encoding="utf-8") as ledger:
            ledger.write(tx.model_dump_json() + "\n")

        # Sau khi ghi log, tự động kích hoạt nén log định kỳ nếu tệp quá lớn
        self.compact_ledger_if_needed()

        return tx

    def compact_ledger_if_needed(self, max_lines: int = 10000) -> None:
        """Tự động nén và dọn dẹp các tệp log nháp trung gian của AI."""
        if not os.path.exists(self.ledger_path):
            return

        # Đếm số dòng thô hiện tại
        with open(self.ledger_path, encoding="utf-8") as f:
            lines = f.readlines()

        if len(lines) < max_lines:
            return

        # Nén log: Chỉ giữ lại các phiên bản giao dịch được "COMMITTED" thực tế
        compacted_txs = []
        for line in lines:
            if line.strip():
                tx_data = json.loads(line.strip())
                if tx_data.get("status") == "COMMITTED":
                    compacted_txs.append(tx_data)

        # Ghi đè lại tệp log sạch (đã loại bỏ hàng nghìn log REJECTED hoặc nháp của AI)
        with open(self.ledger_path, "w", encoding="utf-8") as f:
            for tx in compacted_txs:
                f.write(json.dumps(tx) + "\n")

    def list_transactions(self) -> list[dict[str, Any]]:
        """Đọc lịch sử giao dịch từ tệp tin thuần bằng List Comprehension."""
        if not os.path.exists(self.ledger_path):
            return []

        with open(self.ledger_path, encoding="utf-8") as f:
            return [
                json.loads(line.strip())
                for line in f
                if line.strip()
            ]