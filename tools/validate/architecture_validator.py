import ast
from pathlib import Path


class ArchitectureValidator:
    """Bộ kiểm toán và ép buộc tuân thủ Hiến pháp kiến trúc bằng AST."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.packages_dir = root_dir / "packages"
        self.violations: list[str] = []
        self.dependency_graph: dict[str, set[str]] = {}

    def run_all_checks(self) -> bool:
        """Chạy tất cả các bài kiểm soát ranh giới và cấu trúc."""
        self.violations = []
        self.dependency_graph = {}

        if not self.packages_dir.exists():
            return True

        # 1. Quét AST của toàn bộ các tệp Python trong packages/
        for py_file in self.packages_dir.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue
            self._analyze_file(py_file)

        # 2. Phát hiện quan hệ phụ thuộc vòng (Circular Dependencies)
        self._check_circular_dependencies()

        # 3. Kết luận
        return len(self.violations) == 0

    def _get_module_info(self, file_path: Path) -> tuple[str, str, str] | None:
        """Xác định package name, layer name và file name của tệp."""
        try:
            rel_parts = file_path.relative_to(self.packages_dir).parts
            if len(rel_parts) >= 3:
                package_name = rel_parts[0]
                layer_name = rel_parts[1]
                file_name = rel_parts[-1]
                return package_name, layer_name, file_name
        except ValueError:
            return None
        return None

    def _analyze_file(self, file_path: Path) -> None:
        mod_info = self._get_module_info(file_path)
        if not mod_info:
            return
        package_name, layer_name, file_name = mod_info

        try:
            content = file_path.read_text(encoding="utf-8")
            tree = ast.parse(content)
        except Exception as e:
            self.violations.append(
                f"Syntax Error: Không thể parse AST của {file_path.name}: {e}"
            )
            return

        self._check_imports(tree, file_path, package_name, layer_name)
        self._check_naming_conventions(tree, file_path, layer_name, file_name)

    def _check_imports(
        self, tree: ast.AST, file_path: Path, pkg: str, layer: str
    ) -> None:
        # Độ ưu tiên ranh giới: Thấp không được phụ thuộc Cao
        LAYER_PRIORITY = {
            "domain": 0,
            "application": 1,
            "infrastructure": 2,
        }

        for node in ast.walk(tree):
            imported_module = ""
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_module = alias.name
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported_module = node.module

            if not imported_module:
                continue

            # Chỉ kiểm toán các import nội bộ liên quan đến packages
            # Sửa lỗi SIM102 bằng cách gộp logic and trên một dòng
            is_internal = "packages." in imported_module
            if is_internal and len(imported_module.split(".")) >= 3:
                parts = imported_module.split(".")
                target_pkg = parts[1]
                target_layer = parts[2]

                # Ghi nhận đồ thị phụ thuộc giữa các packages
                if pkg != target_pkg:
                    if pkg not in self.dependency_graph:
                        self.dependency_graph[pkg] = set()
                    self.dependency_graph[pkg].add(target_pkg)

                # Kiểm tra vi phạm phân lớp (Layer Violation)
                self_pri = LAYER_PRIORITY.get(layer.lower(), 99)
                target_pri = LAYER_PRIORITY.get(target_layer.lower(), 99)

                if target_pri > self_pri:
                    self.violations.append(
                        f"Layer Violation: '{file_path.name}' ({layer}) "
                        f"phụ thuộc trái phép vào '{target_layer}' "
                        f"của package '{target_pkg}'."
                    )

            # Chặn hoàn toàn việc Domain hay Application import từ ngoại biên
            # Gộp điều kiện ranh giới (SIM102) và bẻ nhỏ dòng dưới 88 ký tự
            is_ext_leak = (
                "apps." in imported_module or "services." in imported_module
            )
            if is_ext_leak and layer.lower() in ("domain", "application"):
                self.violations.append(
                    f"Wrong Import: Lớp core '{file_path.name}' ({layer}) "
                    f"không được phép import ngoại biên '{imported_module}'."
                )

    def _check_naming_conventions(
        self, tree: ast.AST, file_path: Path, layer: str, file_name: str
    ) -> None:
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name

                # Use Cases trong application layer (Sửa lỗi SIM102 & PIE810)
                is_app_uc = layer == "application" and "use_cases" in file_name
                allowed_app_suffixes = (
                    "UseCase",
                    "Request",
                    "Payload",
                    "Datapoint",
                )
                if is_app_uc and not class_name.endswith(allowed_app_suffixes):
                    self.violations.append(
                        f"Naming Violation: Lớp '{class_name}' trong "
                        f"'{file_name}' bắt buộc phải kết thúc bằng "
                        "'UseCase', 'Request', 'Payload', hoặc 'Datapoint'."
                    )

                # Ports trong domain layer (Sửa lỗi SIM102 & PIE810)
                is_dom_ports = layer == "domain" and "ports" in file_name
                allowed_dom_suffixes = (
                    "Repository",
                    "Port",
                    "Gateway",
                    "Protocol",
                )
                if is_dom_ports and not class_name.endswith(
                    allowed_dom_suffixes
                ):
                    self.violations.append(
                        f"Naming Violation: Lớp '{class_name}' trong "
                        f"'{file_name}' bắt buộc phải kết thúc bằng "
                        "'Repository', 'Port', hoặc 'Gateway'."
                    )

    def _check_circular_dependencies(self) -> None:
        """Phát hiện chu kỳ phụ thuộc (Circular Dependency) bằng DFS."""
        visited: dict[str, int] = {}  # 0: unvisited, 1: visiting, 2: visited

        def dfs(node: str) -> bool:
            visited[node] = 1
            for neighbor in self.dependency_graph.get(node, []):
                if visited.get(neighbor, 0) == 1:
                    self.violations.append(
                        f"Circular Dependency: Phát hiện chu kỳ phụ thuộc vòng "
                        f"giữa hai gói '{node}' và '{neighbor}'."
                    )
                    return True
                # Sửa lỗi SIM102 bằng cách gộp logic and trên một dòng
                if visited.get(neighbor, 0) == 0 and dfs(neighbor):
                    return True
            visited[node] = 2
            return False

        for pkg in list(self.dependency_graph.keys()):
            if visited.get(pkg, 0) == 0:
                dfs(pkg)