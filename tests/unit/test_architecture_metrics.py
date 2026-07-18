import ast
import json
from pathlib import Path
from typing import Any


class ArchitectureMetricsCalculator:
    """Động cơ tính toán chỉ số đo lường chất lượng kiến trúc (Metrics) hằng ngày."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.packages_dir = root_dir / "packages"
        self.output_dir = root_dir / "generated" / "architecture"
        self.metrics: dict[str, dict[str, Any]] = {}
        self.architecture_score: int = 100

    def calculate_all(self) -> bool:
        """Thực thi phân tích mã nguồn và tính toán toàn bộ chỉ số."""
        self.metrics = {}
        if not self.packages_dir.exists():
            return False

        # 1. Trích xuất danh sách các gói hiện có
        packages = sorted(
            [
                p.name
                for p in self.packages_dir.iterdir()
                if p.is_dir() and p.name != "__pycache__"
            ]
        )

        # Khởi tạo ma trận
        import_map: dict[str, set[str]] = {pkg: set() for pkg in packages}
        abstract_map: dict[str, int] = {pkg: 0 for pkg in packages}
        concrete_map: dict[str, int] = {pkg: 0 for pkg in packages}

        # 2. Quét AST tính toán Dependencies và Abstractness hằng ngày
        for pkg in packages:
            pkg_path = self.packages_dir / pkg
            self._scan_package_classes_and_deps(
                pkg, pkg_path, import_map, abstract_map, concrete_map
            )

        # 3. Tính toán các chỉ số Coupling, Instability, Abstraction, Distance
        total_distance = 0.0
        for pkg in packages:
            # Efferent Coupling (Fan-out): Số gói mà pkg này phụ thuộc vào
            ce = len(import_map[pkg])

            # Afferent Coupling (Fan-in): Số gói khác phụ thuộc vào pkg này
            ca = sum(1 for other in packages if pkg in import_map[other])

            # Instability: I = Ce / (Ca + Ce)
            instability = ce / (ca + ce) if (ca + ce) > 0 else 0.0

            # Abstractness: A = Abstract Classes / Total Classes
            abs_count = abstract_map[pkg]
            con_count = concrete_map[pkg]
            total_classes = abs_count + con_count
            abstractness = (
                abs_count / total_classes if total_classes > 0 else 0.0
            )

            # Distance: D = |A + I - 1| (Sai lệch chuỗi chính)
            distance = abs(abstractness + instability - 1.0)
            total_distance += distance

            self.metrics[pkg] = {
                "afferent_coupling_ca": ca,
                "efferent_coupling_ce": ce,
                "instability_i": round(instability, 4),
                "abstractness_a": round(abstractness, 4),
                "distance_d": round(distance, 4),
                "classes": {"abstract": abs_count, "concrete": con_count},
            }

        # 4. Tính toán Điểm Sức Khỏe Kiến Trúc (Architecture Score) quy đổi
        avg_distance = total_distance / len(packages) if packages else 0.0
        # Điểm trừ dựa trên độ lệch Distance trung bình
        deduction = int(avg_distance * 50)
        self.architecture_score = max(0, 100 - deduction)

        # 5. Xuất bản tệp tin báo cáo
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._write_json()
        self._write_markdown()

        return True

    def _scan_package_classes_and_deps(
        self,
        pkg: str,
        pkg_path: Path,
        import_map: dict[str, set[str]],
        abstract_map: dict[str, int],
        concrete_map: dict[str, int],
    ) -> None:
        for py_file in pkg_path.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue

            try:
                content = py_file.read_text(encoding="utf-8")
                tree = ast.parse(content)
            except Exception:
                continue

            for node in ast.walk(tree):
                # Đếm Abstract Classes / Protocols vs Concrete Classes
                if isinstance(node, ast.ClassDef):
                    is_abstract = False
                    for base in node.bases:
                        if (
                            isinstance(base, ast.Name)
                            and base.id in ("Protocol", "ABC")
                        ):
                            is_abstract = True
                        elif (
                            isinstance(base, ast.Attribute)
                            and base.attr in ("Protocol", "ABC")
                        ):
                            is_abstract = True

                    if is_abstract or "ports" in py_file.name:
                        abstract_map[pkg] += 1
                    else:
                        concrete_map[pkg] += 1

                # Ghi nhận dependencies
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
                        if pkg != target_pkg:
                            import_map[pkg].add(target_pkg)

    def _write_json(self) -> None:
        json_file = self.output_dir / "architecture_metrics.json"
        data = {
            "architecture_score": self.architecture_score,
            "packages": self.metrics,
        }
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _write_markdown(self) -> None:
        md_file = self.output_dir / "architecture_metrics.md"
        lines = [
            "# Báo Cáo Đo Lường Chỉ Số Kiến Trúc (Architecture Metrics)",
            "",
            f"**Điểm chất lượng kiến trúc EAOS:** `{self.architecture_score}/100`",
            "",
            "| Gói (Package) | Coupling Ca (In) | Coupling Ce (Out) | Instability (I) | Abstractness (A) | Distance (D) |",
            "| :--- | :---: | :---: | :---: | :---: | :---: |",
        ]
        for pkg, m in self.metrics.items():
            lines.append(
                f"| `{pkg}` | {m['afferent_coupling_ca']} | {m['efferent_coupling_ce']} | "
                f"{m['instability_i']} | {m['abstractness_a']} | `{m['distance_d']}` |"
            )
        lines.append("")

        with open(md_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")