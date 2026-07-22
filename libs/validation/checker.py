import ast
import re
from pathlib import Path

from pydantic import BaseModel


class ADRDocument(BaseModel):
    file_path: str
    title: str
    status: str | None = None
    has_status_header: bool = False
    has_context_header: bool = False
    has_decision_header: bool = False
    has_consequences_header: bool = False


def parse_adr_file(path: Path) -> ADRDocument:
    """Quét và phân tích cấu trúc tiêu đề của các tệp tin ADRs."""
    content = path.read_text(encoding="utf-8")

    has_status = (
        re.search(r"^#+\s+Status", content, re.MULTILINE | re.IGNORECASE)
        is not None
    )
    has_context = (
        re.search(r"^#+\s+Context", content, re.MULTILINE | re.IGNORECASE)
        is not None
    )
    has_decision = (
        re.search(r"^#+\s+Decision", content, re.MULTILINE | re.IGNORECASE)
        is not None
    )
    has_consequences = (
        re.search(r"^#+\s+Consequences", content, re.MULTILINE | re.IGNORECASE)
        is not None
    )

    status_match = re.search(
        r"Status:\s*\*?([a-zA-Z\-]+)\*?", content, re.IGNORECASE
    )
    status = status_match.group(1).strip() if status_match else None

    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else path.name

    return ADRDocument(
        file_path=str(path),
        title=title,
        status=status,
        has_status_header=has_status,
        has_context_header=has_context,
        has_decision_header=has_decision,
        has_consequences_header=has_consequences,
    )


class ASTBoundaryChecker:
    """Trình gác cổng quét AST kiểm tra Layer violations tĩnh."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.packages_dir = root_dir / "packages"
        self.dependency_graph: dict[str, set[str]] = {}

    def scan_dependencies(self) -> dict[str, set[str]]:
        self.dependency_graph = {}
        if not self.packages_dir.exists():
            return {}

        for py_file in self.packages_dir.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue
            self._parse_imports(py_file)

        return self.dependency_graph

    def _parse_imports(self, file_path: Path) -> None:
        try:
            rel_parts = file_path.relative_to(self.packages_dir).parts
            if len(rel_parts) < 3:
                return
            src_pkg = rel_parts[0]
        except ValueError:
            return

        try:
            content = file_path.read_text(encoding="utf-8")
            tree = ast.parse(content)
        except Exception:
            return

        self.dependency_graph.setdefault(src_pkg, set())

        for node in ast.walk(tree):
            imported_module = ""
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_module = alias.name
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_module = node.module

            if imported_module and "packages." in imported_module:
                parts = imported_module.split(".")
                if len(parts) >= 3:
                    target_pkg = parts[1]
                    if src_pkg != target_pkg:
                        self.dependency_graph[src_pkg].add(target_pkg)
