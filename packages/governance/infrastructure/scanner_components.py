import ast
import os
from pathlib import Path

from packages.governance.domain.ports import ScanDiagnostic

"""Single Responsibility Sub-components for Workspace and AST Scanning."""


class WorkspaceWalker:
    """Walker component responsible solely for traversing physical directories."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir: Path = root_dir

    def walk(self) -> tuple[list[Path], int]:
        """Returns tuple of (python_file_paths, empty_directories_count)."""
        py_files: list[Path] = []
        empty_dirs = 0
        exclude = {
            ".git",
            ".venv",
            "venv",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
            "dist",
            "build",
            "node_modules",
            "volumes",
            "runtime",
        }

        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in exclude]
            if not dirs and not files:
                empty_dirs += 1

            # Fixed PERF401: Dùng list.extend thay cho append loop
            py_files.extend(Path(root) / f for f in files if f.endswith(".py"))

        return py_files, empty_dirs


class ASTSafeParser:
    """Parser component responsible solely for AST parsing and error logging."""

    def parse_file(self, file_path: Path) -> tuple[list[tuple[str, str]], ScanDiagnostic | None]:
        """Parses file safely, capturing errors instead of swallowing them."""
        imports: list[tuple[str, str]] = []
        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(content, filename=str(file_path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import | ast.ImportFrom):
                    mod = getattr(node, "module", "") or ""
                    imports.append((str(file_path), mod))
            return imports, None
        except SyntaxError as se:
            diag = ScanDiagnostic(
                file_path=str(file_path),
                severity="ERROR",
                message=f"SyntaxError on line {se.lineno}: {se.msg}",
            )
            return [], diag
        except Exception as e:
            diag = ScanDiagnostic(
                file_path=str(file_path),
                severity="WARNING",
                message=f"File read error: {e}",
            )
            return [], diag
