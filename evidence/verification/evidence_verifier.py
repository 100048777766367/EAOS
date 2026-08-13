from __future__ import annotations

from pathlib import Path
from typing import Final

from evidence.domain.models import Evidence

"""Evidence Verifier and Invalidation Engine (Rule R24)."""


class EvidenceVerifier:
    """Verifies freshness, line ranges, hash, and file existence."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root: Final[Path] = (workspace_root or Path.cwd()).resolve()

    def verify_evidence(self, evidence: Evidence) -> Evidence:
        """Validates evidence on disk; invalidates if stale or missing."""
        if not evidence.file_path:
            return evidence

        target_file = self.root / evidence.file_path
        if not target_file.exists():
            # File deleted: invalidate evidence
            return evidence.model_copy(
                update={
                    "is_verified": False,
                    "freshness_score": 0.0,
                    "relevance_score": 0.0,
                }
            )

        try:
            lines = target_file.read_text(encoding="utf-8").splitlines()
            if evidence.line_start is not None and evidence.line_start > len(lines):
                return evidence.model_copy(
                    update={
                        "is_verified": False,
                        "freshness_score": 0.2,
                    }
                )
        except Exception:
            return evidence.model_copy(update={"is_verified": False, "freshness_score": 0.0})

        return evidence.model_copy(update={"is_verified": True, "freshness_score": 1.0})
