"""EAOS Adaptive Verification Engine."""

from __future__ import annotations

import py_compile
from pathlib import Path

from pydantic import BaseModel, Field


class StageVerificationResult(BaseModel):
    """Result of an individual verification stage."""

    stage_name: str
    command: str
    exit_code: int
    passed: bool
    evidence: str


class PipelineVerificationReport(BaseModel):
    """Report produced by VerificationEngine."""

    overall_passed: bool
    stages: list[StageVerificationResult] = Field(default_factory=list)
    summary: str


class VerificationEngine:
    """Adaptive Verification Engine executing multi-stage pipeline checks."""

    def __init__(self, workspace_root: Path | str = ".") -> None:
        self.workspace_root = Path(workspace_root).resolve()

    def verify_syntax(self, source_roots: list[str] | None = None) -> StageVerificationResult:
        """Run syntax compilation check across Python files."""
        if source_roots is None:
            source_roots = ["apps", "packages", "kernel", "engine", "tools"]

        failed_files: list[str] = []
        total_files = 0
        for root in source_roots:
            target_dir = self.workspace_root / root
            if not target_dir.exists():
                continue
            for py_file in target_dir.rglob("*.py"):
                if any(part.startswith(".") or part in ("venv", "build") for part in py_file.parts):
                    continue
                total_files += 1
                try:
                    py_compile.compile(str(py_file), doraise=True)
                except py_compile.PyCompileError as err:
                    failed_files.append(f"{py_file.name}: {err.msg}")

        passed = len(failed_files) == 0
        evidence = (
            f"Compiled {total_files} Python files cleanly."
            if passed
            else f"Failed syntax compilation on {len(failed_files)} files:\n" + "\n".join(failed_files[:5])
        )
        return StageVerificationResult(
            stage_name="COMPILE_SYNTAX",
            command="python -m py_compile",
            exit_code=0 if passed else 1,
            passed=passed,
            evidence=evidence,
        )

    def run_adaptive_pipeline(self, task_type: str = "CODE") -> PipelineVerificationReport:
        """Run adaptive verification pipeline based on task type."""
        stages: list[StageVerificationResult] = []

        # 1. Compile stage
        compile_res = self.verify_syntax()
        stages.append(compile_res)

        overall_passed = all(s.passed for s in stages)
        summary = (
            f"Adaptive Pipeline ({task_type}): {'PASS' if overall_passed else 'FAIL'} "
            f"[{sum(1 for s in stages if s.passed)}/{len(stages)} stages passed]"
        )
        return PipelineVerificationReport(
            overall_passed=overall_passed,
            stages=stages,
            summary=summary,
        )
