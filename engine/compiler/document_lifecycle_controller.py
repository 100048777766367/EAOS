import hashlib
from datetime import UTC, datetime
from pathlib import Path


class DocumentLifecycleController:
    """Động cơ quản lý vòng đời tài liệu tự trị (Document Lifecycle Controller)."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.archive_dir = root_dir / "generated" / "docs" / "archive"
        self.archive_dir.mkdir(parents=True, exist_ok=True)

    def transition_state(
        self, doc_path: Path, target_status: str, reason: str | None = None
    ) -> bool:
        """Thực thi chuyển trạng thái vòng đời, tự động sao lưu lịch sử."""
        if not doc_path.exists():
            return False

        content = doc_path.read_text(encoding="utf-8")
        clean_name = doc_path.stem

        # 1. BẢN SAO SỐ (Archiving): Sao chụp trạng thái cũ trước khi đổi
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        target_archive = self.archive_dir / clean_name
        target_archive.mkdir(parents=True, exist_ok=True)

        backup_file = target_archive / f"{timestamp}_{doc_path.name}"
        with open(backup_file, "w", encoding="utf-8") as f:
            f.write(content)

        # 2. CRYPTOGRAPHIC FIXITY
        sha256_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

        # 3. METADATA SYNCHRONIZATION (Front-matter YAML)
        status_upper = target_status.upper()
        today_str = datetime.now(UTC).strftime("%Y-%m-%d")

        reason_line = f"reason_suspended: {reason}\n" if reason else ""
        new_front_matter = (
            "---\n"
            f"title: {doc_path.stem.replace('_', ' ').title()}\n"
            f"status: {status_upper}\n"
            f"{reason_line}"
            f"last_updated: {today_str}\n"
            f"fixity_hash: {sha256_hash}\n"
            "---"
        )

        if content.startswith("---"):
            parts = content.split("---", 2)
            # Sửa lỗi SIM108 bằng toán tử ba ngôi hiện đại
            updated_content = (
                new_front_matter + parts[2]
                if len(parts) >= 3
                else new_front_matter + "\n\n" + content
            )
        else:
            updated_content = new_front_matter + "\n\n" + content

        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(updated_content)

        return True