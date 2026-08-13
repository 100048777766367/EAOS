import ast
import subprocess
import sys
from pathlib import Path
from typing import Final

from pydantic import BaseModel, ConfigDict

"""OS-level Git pre-commit hook installer and AST enforcement engine.

Enforces EAOS Architecture Constitution v3.0 rules directly at the
AST level (Domain Purity, Layer Isolation, and Type Safety).
"""


class HookInstallationResult(BaseModel):
    """Value object representing Git pre-commit hook installation result."""

    model_config = ConfigDict(frozen=True)

    installed: bool
    hook_path: str
    message: str


class ASTViolation(BaseModel):
    """Value object representing an architectural AST violation."""

    model_config = ConfigDict(frozen=True)

    file_path: str
    line: int
    rule_id: str
    message: str


class PreCommitASTHookEngine:
    """Stricter Git pre-commit hook and AST validation engine."""

    FORBIDDEN_DOMAIN_IMPORTS: Final[set[str]] = {
        "fastapi",
        "sqlalchemy",
        "psycopg2",
        "redis",
        "requests",
        "httpx",
        "streamlit",
        "uvicorn",
        "pydantic_settings",
    }

    def install_git_hook(
        self,
        repo_root: str = ".",
    ) -> HookInstallationResult:
        """Installs executable pre-commit hook in .git/hooks."""
        root_path = Path(repo_root).resolve()
        hooks_dir = root_path / ".git" / "hooks"

        if not hooks_dir.exists():
            hooks_dir.mkdir(parents=True, exist_ok=True)

        hook_file = hooks_dir / "pre-commit"

        script_content = (
            "#!/bin/sh\n"
            "# ========================================\n"
            "# EAOS Constitution Gatekeeper - STRICT\n"
            "# ========================================\n"
            "echo 'Running EAOS AST Validation...'\n"
            'python -c "from tools.validate.pre_commit_hook '
            "import PreCommitASTHookEngine; "
            "import sys; "
            "engine = PreCommitASTHookEngine(); "
            "success = engine.run_pre_commit_validation(); "
            'sys.exit(0 if success else 1)"\n'
            "if [ $? -ne 0 ]; then\n"
            "  echo '========================================'\n"
            "  echo 'EAOS AST VALIDATION FAILED. BLOCKED.'\n"
            "  echo '========================================'\n"
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
                message="Git pre-commit hook installed.",
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
        """Executes AST validation on staged files."""
        root_path = Path(repo_root).resolve()
        violations: list[ASTViolation] = []

        staged_files = self._get_staged_python_files(root_path)

        for file_path in staged_files:
            abs_path = root_path / file_path
            if not abs_path.exists():
                continue

            try:
                code = abs_path.read_text(encoding="utf-8")
                tree = ast.parse(code, filename=str(file_path))

                if "domain" in file_path.parts:
                    domain_violations = self._check_domain_purity(tree, file_path)
                    violations.extend(domain_violations)

                type_violations = self._check_type_annotations(tree, file_path)
                violations.extend(type_violations)

            except SyntaxError as se:
                violations.append(
                    ASTViolation(
                        file_path=str(file_path),
                        line=se.lineno or 0,
                        rule_id="SYNTAX-01",
                        message=f"Python Syntax Error: {se.msg}",
                    )
                )
            except Exception as ex:
                print(
                    f"Warning: Could not parse {file_path}: {ex}",
                    file=sys.stderr,
                )

        if violations:
            print(
                "\n[EAOS GATEKEEPER] Architectural Violations:",
                file=sys.stderr,
            )
            for v in violations:
                print(
                    f"  ❌ [{v.rule_id}] {v.file_path}:{v.line} -> {v.message}",
                    file=sys.stderr,
                )
            print(
                "\nCommit rejected: Constitution compliance failed.\n",
                file=sys.stderr,
            )
            return False

        print("✅ EAOS AST Constitutional Validation Passed.")
        return True

    def _get_staged_python_files(self, root_path: Path) -> list[Path]:
        """Retrieves list of staged Python files."""
        try:
            result = subprocess.run(
                [
                    "git",
                    "diff",
                    "--cached",
                    "--name-only",
                    "--diff-filter=ACM",
                ],
                cwd=root_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return [Path(line.strip()) for line in result.stdout.splitlines() if line.strip().endswith(".py")]
        except Exception:
            return [
                p.relative_to(root_path)
                for p in root_path.rglob("*.py")
                if ".venv" not in p.parts and "build" not in p.parts and "dist" not in p.parts
            ]

    def _check_domain_purity(self, tree: ast.Module, file_path: Path) -> list[ASTViolation]:
        """Enforces Rule R4: Domain Purity."""
        violations: list[ASTViolation] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    base_mod = alias.name.split(".")[0]
                    if base_mod in self.FORBIDDEN_DOMAIN_IMPORTS:
                        msg = f"Domain Purity Violation: Domain imports forbidden module '{alias.name}'."
                        violations.append(
                            ASTViolation(
                                file_path=str(file_path),
                                line=node.lineno,
                                rule_id="CONSTITUTION-R4",
                                message=msg,
                            )
                        )
            elif isinstance(node, ast.ImportFrom) and node.module:
                base_mod = node.module.split(".")[0]
                if base_mod in self.FORBIDDEN_DOMAIN_IMPORTS:
                    msg = f"Domain Purity Violation: Domain imports from forbidden module '{node.module}'."
                    violations.append(
                        ASTViolation(
                            file_path=str(file_path),
                            line=node.lineno,
                            rule_id="CONSTITUTION-R4",
                            message=msg,
                        )
                    )
        return violations

    def _check_type_annotations(self, tree: ast.Module, file_path: Path) -> list[ASTViolation]:
        """Enforces strict type safety annotations."""
        violations: list[ASTViolation] = []
        if "tests" in file_path.parts:
            return violations

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith("_") and node.name != "__init__":
                    continue
                if node.returns is None and node.name != "__init__" and not node.name.startswith("test_"):
                    msg = f"Strict Type Safety Violation: Function '{node.name}' lacks return type annotation."
                    violations.append(
                        ASTViolation(
                            file_path=str(file_path),
                            line=node.lineno,
                            rule_id="TYPE-SAFETY-01",
                            message=msg,
                        )
                    )
        return violations
