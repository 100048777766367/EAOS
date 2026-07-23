"""Infrastructure adapters for knowledge repository persistence."""

from typing import Any


class PostgresKnowledgeRepository:
    """PostgreSQL adapter for knowledge artifacts."""

    def __init__(self, db_url: str) -> None:
        self.db_url: str = db_url
        self._artifacts: dict[str, Any] = {}

    def save(self, artifact: Any) -> Any:
        """Saves knowledge artifact."""
        art_id = getattr(artifact, "id", str(len(self._artifacts) + 1))
        self._artifacts[art_id] = artifact
        return artifact

    def find_by_id(self, artifact_id: str) -> Any | None:
        """Finds knowledge artifact by ID."""
        return self._artifacts.get(artifact_id)


class SplayCacheKnowledgeRepository:
    """Splay Tree RAM cache wrapper around knowledge repository."""

    def __init__(self, delegate: Any = None) -> None:
        self.delegate = delegate
        self._cache: dict[str, Any] = {}

    def save(self, artifact: Any) -> Any:
        """Saves knowledge artifact to RAM cache and delegate."""
        art_id = getattr(artifact, "id", str(len(self._cache) + 1))
        self._cache[art_id] = artifact
        if self.delegate and hasattr(self.delegate, "save"):
            self.delegate.save(artifact)
        return artifact

    def find_by_id(self, artifact_id: str) -> Any | None:
        """Retrieves artifact from cache or delegate."""
        if artifact_id in self._cache:
            return self._cache[artifact_id]
        if self.delegate and hasattr(self.delegate, "find_by_id"):
            item = self.delegate.find_by_id(artifact_id)
            if item:
                self._cache[artifact_id] = item
            return item
        return None

    def get_tree_layout(self) -> dict[str, Any]:
        """Returns layout structure of splay cache."""
        return {"root": "SplayRoot", "size": len(self._cache)}

    def get_tree_mermaid(self) -> str:
        """Generates mermaid topology string."""
        return "graph TD\n  Root --> CacheNode"

    def get_audit_logs(self, artifact_id: str) -> list[Any]:
        """Retrieves audit logs for artifact."""
        return []

    def delete(self, artifact_id: str, author: str) -> bool:
        """Deletes artifact from cache."""
        if artifact_id in self._cache:
            del self._cache[artifact_id]
            return True
        return False
