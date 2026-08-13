from __future__ import annotations

from packages.harness.domain.actions import SemanticActionType

"""Semantic Classifier parsing command intent without LLMs (Rule R38)."""


class SemanticClassifier:
    """Classifies raw commands into semantic action types and risk levels."""

    DESTRUCTIVE_PATTERNS = {  # noqa: RUF012
        "rm -rf",
        "git reset",
        "git clean",
        "drop table",
        "push --force",
        "chmod 777",
        "overwrite",
    }

    def classify_intent(self, action_name: str, target_uri: str) -> tuple[SemanticActionType, bool]:
        """Returns (SemanticActionType, is_destructive)."""
        combined = f"{action_name} {target_uri}".lower()

        for pat in self.DESTRUCTIVE_PATTERNS:
            if pat in combined:
                if "git" in pat:
                    return SemanticActionType.GIT_MUTATE, True
                if "drop" in pat:
                    return SemanticActionType.DB_MUTATE, True
                return SemanticActionType.SHELL_DESTRUCTIVE, True

        if any(k in combined for k in ("delete", "remove", "unlink")):
            return SemanticActionType.FS_DELETE, True

        if any(k in combined for k in ("write", "edit", "update", "patch")):
            return SemanticActionType.FS_WRITE, False

        return SemanticActionType.FS_READ, False
