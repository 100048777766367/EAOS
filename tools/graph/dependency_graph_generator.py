import ast
import json
from pathlib import Path


class DependencyGraphGenerator:
    """Động cơ phân tích AST và tự động xuất bản đồ quan hệ phụ thuộc."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.packages_dir = root_dir / "packages"
        self.output_dir = root_dir / "generated" / "architecture"
        self.graph: dict[str, list[str]] = {}

    def generate(self) -> bool:
        """Quét mã nguồn và xuất bản đồ định dạng Mermaid, Graphviz, JSON."""
        self.graph = {}
        if not self.packages_dir.exists():
            return False

        # 1. Quét toàn bộ import của các tệp tin Python trong packages/
        for py_file in self.packages_dir.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue
            self._parse_file_imports(py_file)

        # Sắp xếp và làm sạch đồ thị
        self.graph = {
            pkg: sorted(list(deps)) for pkg, deps in self.graph.items()
        }

        # 2. Tạo thư mục output generated/
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 3. Xuất các định dạng tệp tin đích
        self._write_json()
        self._write_dot()
        self._write_mermaid_md()

        return True

    def _parse_file_imports(self, file_path: Path) -> None:
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

        if src_pkg not in self.graph:
            self.graph[src_pkg] = []

        deps_set = set(self.graph[src_pkg])

        for node in ast.walk(tree):
            imported_module = ""
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_module = alias.name
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_module = node.module

            if not imported_module:
                continue

            if "packages." in imported_module:
                parts = imported_module.split(".")
                if len(parts) >= 3:
                    target_pkg = parts[1]
                    if src_pkg != target_pkg:
                        deps_set.add(target_pkg)

        self.graph[src_pkg] = list(deps_set)

    def _write_json(self) -> None:
        json_file = self.output_dir / "dependency_graph.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(self.graph, f, indent=2, ensure_ascii=False)

    def _write_dot(self) -> None:
        dot_file = self.output_dir / "dependency_graph.dot"
        lines = [
            "digraph G {",
            "    rankdir=TB;",
            "    node [shape=box, style=filled, color=lightblue];",
        ]
        for pkg, deps in self.graph.items():
            clean_pkg = pkg.replace("-", "_")
            lines.append(f'    {clean_pkg} [label="{pkg}"];')
            for dep in deps:
                clean_dep = dep.replace("-", "_")
                lines.append(f"    {clean_pkg} -> {clean_dep};")
        lines.append("}")

        with open(dot_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    def _write_mermaid_md(self) -> None:
        md_file = self.output_dir / "dependency_graph.md"
        lines = [
            "# Sơ Đồ Quan Hệ Phụ Thuộc EAOS (Dependency Graph)",
            "",
            "Bản đồ này được tự động tạo lập từ phân tích AST.",
            "",
            "```mermaid",
            "graph TD",
        ]
        for pkg, deps in self.graph.items():
            clean_pkg = pkg.replace("-", "_")
            lines.append(f'    {clean_pkg}["{pkg}"]')
            for dep in deps:
                clean_dep = dep.replace("-", "_")
                lines.append(f"    {clean_pkg} --> {clean_dep}")
        lines.append("```")
        lines.append("")

        with open(md_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")