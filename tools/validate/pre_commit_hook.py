"""OS-level Git pre-commit hook installer and AST enforcement engine."""

import sys
from pathlib import Path

from pydantic import BaseModel, ConfigDict


class HookInstallationResult(BaseModel):
    """Value object representing Git pre-commit hook installation result."""

    model_config = ConfigDict(frozen=True)

    installed: bool
    hook_path: str
    message: str


class PreCommitASTHookEngine:
    """Git pre-commit hook installer and AST validation enforcement engine."""

    def install_git_hook(
        self,
        repo_root: str = ".",
    ) -> HookInstallationResult:
        """Installs executable pre-commit hook in .git/hooks directory."""
        root_path = Path(repo_root).resolve()
        hooks_dir = root_path / ".git" / "hooks"

        if not hooks_dir.exists():
            hooks_dir.mkdir(parents=True, exist_ok=True)

        hook_file = hooks_dir / "pre-commit"
        script_content = (
            "#!/bin/sh\n"
            "# EAOS Architecture Constitution Gatekeeper Hook\n"
            "uv run task validate\n"
            "if [ $? -ne 0 ]; then\n"
            "  echo 'EAOS AST Validation Failed. Commit Blocked.'\n"
            "  exit 1\n"
            "fi\n"
        )

        try:
            hook_file.write_text(script_content, encoding="utf-8")
            if hasattr(sys, "chmod"):
                hook_file.chmod(0o755)

            return HookInstallationResult(
                installed=True,
                hook_path=str(hook_file),
                message="Git pre-commit hook installed successfully.",
            )
        except Exception as exc:
            return HookInstallationResult(
                installed=False,
                hook_path=str(hook_file),
                message=f"Hook installation error: {exc!s}",
            )

    def run_pre_commit_validation(
        self,
        repo_root: str = ".",
    ) -> bool:
        """Executes AST boundary validation on repository files."""
        from services.validator.engine import EAOSValidatorEngine

        engine = EAOSValidatorEngine(Path(repo_root).resolve())
        report = engine.run_validation()
        return report.overall_passed
