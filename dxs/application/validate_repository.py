from __future__ import annotations

from pathlib import Path

from dxs.domain.repository import RepositoryContext
from dxs.domain.validation import (
    ValidationResult,
    ValidationStatus,
)


class RepositoryValidator:
    """Validate EAOS repository against discovered sources."""

    def validate(
        self,
        context: RepositoryContext,
    ) -> list[ValidationResult]:
        results: list[ValidationResult] = []

        results.extend(self._validate_sources(context))

        results.extend(self._validate_architecture_constitution(context))

        results.extend(self._validate_repository_contract(context))

        results.extend(self._validate_repository_specification(context))

        results.extend(self._validate_adr_index(context))

        return results

    def _validate_sources(
        self,
        context: RepositoryContext,
    ) -> list[ValidationResult]:
        results: list[ValidationResult] = []

        for document in context.documents:
            if document.exists:
                results.append(
                    ValidationResult(
                        check=f"source.{document.key}",
                        status=ValidationStatus.PASS,
                        message="Authoritative source found.",
                        path=str(document.path),
                    )
                )
            else:
                results.append(
                    ValidationResult(
                        check=f"source.{document.key}",
                        status=ValidationStatus.FAIL,
                        message="Authoritative source is missing.",
                        path=str(document.path),
                    )
                )

        return results

    def _validate_architecture_constitution(
        self,
        context: RepositoryContext,
    ) -> list[ValidationResult]:
        document = context.architecture_constitution

        if not document.exists:
            return []

        return self._validate_non_empty(
            check="architecture.constitution",
            path=document.path,
            required_markers=("Architecture Constitution",),
        )

    def _validate_repository_contract(
        self,
        context: RepositoryContext,
    ) -> list[ValidationResult]:
        document = context.repository_contract

        if not document.exists:
            return []

        return self._validate_non_empty(
            check="repository.contract",
            path=document.path,
            required_markers=(),
        )

    def _validate_repository_specification(
        self,
        context: RepositoryContext,
    ) -> list[ValidationResult]:
        document = context.repository_specification

        if not document.exists:
            return []

        return self._validate_non_empty(
            check="repository.specification",
            path=document.path,
            required_markers=(),
        )

    def _validate_adr_index(
        self,
        context: RepositoryContext,
    ) -> list[ValidationResult]:
        document = context.adr_index

        if not document.exists:
            return []

        return self._validate_non_empty(
            check="architecture.adr_index",
            path=document.path,
            required_markers=(),
        )

    @staticmethod
    def _validate_non_empty(
        *,
        check: str,
        path: Path,
        required_markers: tuple[str, ...],
    ) -> list[ValidationResult]:
        try:
            content = path.read_text(encoding="utf-8-sig").strip()
        except OSError as exc:
            return [
                ValidationResult(
                    check=check,
                    status=ValidationStatus.FAIL,
                    message=f"Cannot read source: {exc}",
                    path=str(path),
                )
            ]

        if not content:
            return [
                ValidationResult(
                    check=check,
                    status=ValidationStatus.FAIL,
                    message="Source document is empty.",
                    path=str(path),
                )
            ]

        results = [
            ValidationResult(
                check=check,
                status=ValidationStatus.PASS,
                message="Source document is readable and non-empty.",
                path=str(path),
            )
        ]

        results.extend(
            ValidationResult(
                check=f"{check}.marker",
                status=ValidationStatus.WARN,
                message=f"Expected marker not found: {marker}",
                path=str(path),
            )
            for marker in required_markers
            if marker not in content
        )

        return results
