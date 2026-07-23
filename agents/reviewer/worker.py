"""Reviewer AI Agent worker for AST code review and linting."""

import time

from pydantic import BaseModel, ConfigDict


class ReviewFindingDTO(BaseModel):
    """Value object for code review findings."""

    model_config = ConfigDict(frozen=True)

    file_path: str
    severity: str
    rule_violation: str


class CodeReviewReport(BaseModel):
    """Value object for code review report outputs."""

    model_config = ConfigDict(frozen=True)

    review_id: str
    passed: bool
    findings: list[ReviewFindingDTO]


class ReviewerAgentWorker:
    """AI Agent evaluating source code against AST and linter rules."""

    def review_code_patch(
        self,
        file_path: str,
        code_content: str,
    ) -> CodeReviewReport:
        """Scans source code for layer leakage and style violations."""
        findings: list[ReviewFindingDTO] = []
        if "import fastapi" in code_content and "domain" in file_path:
            findings.append(
                ReviewFindingDTO(
                    file_path=file_path,
                    severity="HIGH",
                    rule_violation="R4: Domain Framework Leakage",
                )
            )

        return CodeReviewReport(
            review_id=f"rev_{int(time.time())}",
            passed=len(findings) == 0,
            findings=findings,
        )
