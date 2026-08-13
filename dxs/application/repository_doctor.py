from __future__ import annotations

from dxs.domain.repository import RepositoryContext


class RepositoryDoctor:
    """Validate discovered EAOS repository sources."""

    def inspect(
        self,
        context: RepositoryContext,
    ) -> list[str]:
        results: list[str] = []

        for document in context.documents:
            if document.exists:
                results.append(f"[PASS] {document.key}: {document.path} ({document.role})")
            else:
                results.append(f"[WARN] {document.key}: missing at {document.path} ({document.role})")

        return results
