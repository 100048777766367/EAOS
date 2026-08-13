from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

# ============================================================================
# DXS Repository Doctor v2
# ============================================================================


@dataclass(frozen=True)
class RuleResult:
    rule_id: str
    category: str
    name: str
    passed: bool
    message: str
    file: Path | None = None
    line: int | None = None


class ArchitectureChecker:
    """
    Static architecture and repository governance checker for EAOS DXS.

    Architecture:

        CLI
         ↓
        Application
         ↓
        Domain
         ↑
        Ports
         ↑
        Adapters

    Dependency direction:

        CLI → Application → Domain
                    ↓
                  Ports
                    ↑
                 Adapters
    """

    LAYERS = (
        "domain",
        "ports",
        "application",
        "adapters",
        "cli",
    )

    # Lower number = more inward / more stable.
    LAYER_ORDER: ClassVar[dict[str, int]] = {
        "domain": 0,
        "ports": 1,
        "application": 2,
        "adapters": 3,
        "cli": 4,
    }

    # Framework / infrastructure packages that Domain must never import.
    DOMAIN_FORBIDDEN_IMPORTS: ClassVar[set[str]] = {
        "fastapi",
        "flask",
        "django",
        "typer",
        "click",
        "rich",
        "pydantic",
        "sqlalchemy",
        "alembic",
        "redis",
        "networkx",
        "requests",
        "httpx",
        "aiohttp",
        "boto3",
        "docker",
        "git",
        "subprocess",
    }

    PORTS_FORBIDDEN_IMPORTS: ClassVar[set[str]] = {
        "fastapi",
        "flask",
        "django",
        "typer",
        "click",
        "rich",
        "sqlalchemy",
        "alembic",
        "redis",
        "networkx",
        "boto3",
        "docker",
    }

    APPLICATION_FORBIDDEN_IMPORTS: ClassVar[set[str]] = {
        "fastapi",
        "flask",
        "django",
        "typer",
        "click",
        "rich",
        "sqlalchemy",
        "alembic",
        "redis",
        "networkx",
        "boto3",
        "docker",
    }

    # Direct imports from adapters are forbidden in Application.
    APPLICATION_FORBIDDEN_MODULES: ClassVar[set[str]] = {
        "dxs.adapters",
    }

    # CLI should not directly access infrastructure.
    CLI_FORBIDDEN_MODULES: ClassVar[set[str]] = {
        "dxs.adapters",
    }

    REQUIRED_PACKAGE_FILES: ClassVar[dict[str, str]] = {
        "domain": "__init__.py",
        "ports": "__init__.py",
        "application": "__init__.py",
        "adapters": "__init__.py",
        "cli": "__init__.py",
    }

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.results: list[RuleResult] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self) -> list[RuleResult]:
        self.results.clear()

        self._check_root()
        self._check_required_packages()
        self._check_python_files()

        return self.results

    def passed(self) -> bool:
        return all(result.passed for result in self.results)

    # ------------------------------------------------------------------
    # Repository checks
    # ------------------------------------------------------------------

    def _check_root(self) -> None:
        passed = self.root.exists() and self.root.is_dir()

        self._result(
            rule_id="DXS-REPO-001",
            category="Repository",
            name="DXS Root",
            passed=passed,
            message=("DXS root exists." if passed else f"DXS root does not exist: {self.root}"),
        )

    def _check_required_packages(self) -> None:
        for layer, filename in self.REQUIRED_PACKAGE_FILES.items():
            directory = self.root / layer
            package_file = directory / filename

            passed = directory.is_dir() and package_file.is_file()

            self._result(
                rule_id="DXS-REPO-002",
                category="Repository",
                name=f"Package Boundary: {layer}",
                passed=passed,
                message=(
                    f"{layer}/ package boundary is valid."
                    if passed
                    else f"Missing required package file: {package_file}"
                ),
                file=package_file,
            )

    def _check_python_files(self) -> None:
        for layer in self.LAYERS:
            layer_path = self.root / layer

            if not layer_path.is_dir():
                continue

            for source_file in layer_path.rglob("*.py"):
                if source_file.name == "__init__.py":
                    continue

                self._check_python_file(layer, source_file)

    # ------------------------------------------------------------------
    # Python checks
    # ------------------------------------------------------------------

    def _check_python_file(
        self,
        layer: str,
        source_file: Path,
    ) -> None:
        try:
            source = source_file.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(source_file))
        except (OSError, SyntaxError) as exc:
            self._result(
                rule_id="DXS-REPO-003",
                category="Repository",
                name="Python Syntax",
                passed=False,
                message=f"Cannot parse Python file: {exc}",
                file=source_file,
            )
            return

        self._check_imports(layer, source_file, tree)

    # ------------------------------------------------------------------
    # Import checks
    # ------------------------------------------------------------------

    def _check_imports(
        self,
        layer: str,
        source_file: Path,
        tree: ast.AST,
    ) -> None:
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self._check_import(
                        layer=layer,
                        source_file=source_file,
                        line=node.lineno,
                        module=alias.name,
                    )

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""

                if module:
                    self._check_import(
                        layer=layer,
                        source_file=source_file,
                        line=node.lineno,
                        module=module,
                    )

                self._check_relative_import(
                    layer=layer,
                    source_file=source_file,
                    node=node,
                )

    def _check_import(
        self,
        layer: str,
        source_file: Path,
        line: int,
        module: str,
    ) -> None:
        root_module = module.split(".")[0]

        # --------------------------------------------------------------
        # Domain purity
        # --------------------------------------------------------------

        if layer == "domain" and root_module in self.DOMAIN_FORBIDDEN_IMPORTS:
            self._result(
                rule_id="DXS-ARCH-001",
                category="Architecture",
                name="Domain Independence",
                passed=False,
                message=(f"Domain must not import infrastructure/framework ''{root_module}''."),
                file=source_file,
                line=line,
            )
            return

        # --------------------------------------------------------------
        # Ports purity
        # --------------------------------------------------------------

        if layer == "ports" and root_module in self.PORTS_FORBIDDEN_IMPORTS:
            self._result(
                rule_id="DXS-ARCH-003",
                category="Architecture",
                name="Port Isolation",
                passed=False,
                message=(f"Ports must not import infrastructure/framework ''{root_module}''."),
                file=source_file,
                line=line,
            )
            return

        # --------------------------------------------------------------
        # Application purity
        # --------------------------------------------------------------

        if layer == "application" and root_module in self.APPLICATION_FORBIDDEN_IMPORTS:
            self._result(
                rule_id="DXS-ARCH-005",
                category="Architecture",
                name="Application Boundary",
                passed=False,
                message=(f"Application must not directly import infrastructure ''{root_module}''."),
                file=source_file,
                line=line,
            )
            return

        if layer == "application" and any(
            module == forbidden or module.startswith(f"{forbidden}.")
            for forbidden in self.APPLICATION_FORBIDDEN_MODULES
        ):
            self._result(
                rule_id="DXS-ARCH-005",
                category="Architecture",
                name="Application Boundary",
                passed=False,
                message=("Application must not directly depend on adapters."),
                file=source_file,
                line=line,
            )
            return

        # --------------------------------------------------------------
        # CLI boundary
        # --------------------------------------------------------------

        if layer == "cli" and any(
            module == forbidden or module.startswith(f"{forbidden}.") for forbidden in self.CLI_FORBIDDEN_MODULES
        ):
            self._result(
                rule_id="DXS-ARCH-006",
                category="Architecture",
                name="CLI Boundary",
                passed=False,
                message="CLI must not directly access adapters.",
                file=source_file,
                line=line,
            )
            return

        # --------------------------------------------------------------
        # Internal dependency direction
        # --------------------------------------------------------------

        if module.startswith("dxs."):
            imported_layer = self._detect_layer(module)

            if imported_layer is not None:
                self._check_dependency_direction(
                    source_layer=layer,
                    imported_layer=imported_layer,
                    source_file=source_file,
                    line=line,
                    module=module,
                )

    def _check_relative_import(
        self,
        layer: str,
        source_file: Path,
        node: ast.ImportFrom,
    ) -> None:
        if node.level <= 0:
            return

        # Domain should remain simple and not traverse arbitrary package
        # boundaries with deep relative imports.
        if layer == "domain" and node.level > 1:
            self._result(
                rule_id="DXS-ARCH-002",
                category="Architecture",
                name="Domain Boundary",
                passed=False,
                message="Domain contains a deep relative import.",
                file=source_file,
                line=node.lineno,
            )

    # ------------------------------------------------------------------
    # Dependency direction
    # ------------------------------------------------------------------

    def _check_dependency_direction(
        self,
        source_layer: str,
        imported_layer: str,
        source_file: Path,
        line: int,
        module: str,
    ) -> None:
        source_level = self.LAYER_ORDER[source_layer]
        imported_level = self.LAYER_ORDER[imported_layer]

        # Domain must never depend on anything outside itself.
        if source_layer == "domain" and imported_layer != "domain":
            self._result(
                rule_id="DXS-ARCH-002",
                category="Architecture",
                name="Dependency Direction",
                passed=False,
                message=(f"Domain depends on {imported_layer}: {module}"),
                file=source_file,
                line=line,
            )
            return

        # Ports may depend on Domain, but not outward.
        if source_layer == "ports" and imported_layer not in {
            "domain",
            "ports",
        }:
            self._result(
                rule_id="DXS-ARCH-003",
                category="Architecture",
                name="Port Isolation",
                passed=False,
                message=(f"Ports depend on outward layer {imported_layer}: {module}"),
                file=source_file,
                line=line,
            )
            return

        # Application may depend on Domain and Ports.
        if source_layer == "application" and imported_layer not in {
            "domain",
            "ports",
            "application",
        }:
            self._result(
                rule_id="DXS-ARCH-005",
                category="Architecture",
                name="Application Boundary",
                passed=False,
                message=(f"Application depends on outward layer {imported_layer}: {module}"),
                file=source_file,
                line=line,
            )
            return

        # Adapters can depend inward.
        if source_layer == "adapters" and imported_layer in {
            "application",
            "domain",
            "ports",
            "adapters",
        }:
            return

        # CLI can depend on Application and inward layers.
        if source_layer == "cli" and imported_layer in {
            "application",
            "domain",
            "ports",
            "cli",
        }:
            return

        # Generic outward dependency check.
        if imported_level < source_level:
            return

        if source_layer == imported_layer:
            return

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _detect_layer(self, module: str) -> str | None:
        parts = module.split(".")

        if len(parts) < 2:
            return None

        layer = parts[1]

        if layer in self.LAYERS:
            return layer

        return None

    def _result(
        self,
        rule_id: str,
        category: str,
        name: str,
        passed: bool,
        message: str,
        file: Path | None = None,
        line: int | None = None,
    ) -> None:
        self.results.append(
            RuleResult(
                rule_id=rule_id,
                category=category,
                name=name,
                passed=passed,
                message=message,
                file=file,
                line=line,
            )
        )

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def print_report(self) -> int:
        results = self.run()

        print()
        print("=" * 80)
        print("EAOS / DXS REPOSITORY DOCTOR")
        print("=" * 80)
        print()

        if not results:
            print("No rules were executed.")
            return 1

        passed = sum(result.passed for result in results)
        failed = len(results) - passed

        grouped: dict[str, list[RuleResult]] = {}

        for result in results:
            grouped.setdefault(result.category, []).append(result)

        for category, category_results in grouped.items():
            print(category)

            for result in category_results:
                status = "PASS" if result.passed else "FAIL"

                print(f"  {result.rule_id:<14} {status:<5} {result.name}")

                if not result.passed:
                    location = ""

                    if result.file is not None:
                        try:
                            relative = result.file.relative_to(self.root)
                        except ValueError:
                            relative = result.file

                        location = str(relative)

                        if result.line is not None:
                            location += f":{result.line}"

                    if location:
                        print(f"                 {location}")

                    print(f"                 {result.message}")

            print()

        print("-" * 80)
        print(f"Rules executed : {len(results)}")
        print(f"Passed         : {passed}")
        print(f"Failed         : {failed}")
        print()

        if failed == 0:
            print(f"PASS — {passed}/{len(results)} architecture/governance rules passed.")
            return 0

        print(f"FAIL — {failed}/{len(results)} architecture/governance rules failed.")

        return 1


def main() -> int:
    """
    CLI entry point for direct execution.
    """
    dxs_root = Path(__file__).resolve().parents[1]

    checker = ArchitectureChecker(dxs_root)

    return checker.print_report()


if __name__ == "__main__":
    raise SystemExit(main())
