from __future__ import annotations

from pathlib import Path

"""EAOS Repository Package Scanner & Provisioner.

Scans for missing __init__.py, README.md, and pyproject.toml files.
"""


class PackageRepositoryScanner:
    """Scans and provisions missing Python package artifacts."""

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root = (root_dir or Path("D:/EAOS")).resolve()

    def scan_and_provision(self) -> dict[str, int]:
        """Scan repository and create missing package files."""
        added_inits = self._ensure_init_py_files()
        added_readmes = self._ensure_package_readmes()
        added_configs = self._ensure_app_configs()

        return {
            "added_inits": added_inits,
            "added_readmes": added_readmes,
            "added_configs": added_configs,
        }

    def _ensure_init_py_files(self) -> int:
        """Ensure all Python package directories have __init__.py."""
        count = 0
        scan_roots = [self.root / "packages", self.root / "apps"]

        for scan_root in scan_roots:
            if not scan_root.exists():
                continue
            for dir_path in scan_root.rglob("*"):
                if not dir_path.is_dir():
                    continue
                if dir_path.name in {
                    "__pycache__",
                    ".venv",
                    "runtime",
                    ".git",
                }:
                    continue

                has_py = any(dir_path.glob("*.py"))
                has_subdirs = any(p.is_dir() and p.name != "__pycache__" for p in dir_path.iterdir())

                if has_py or has_subdirs:
                    init_file = dir_path / "__init__.py"
                    if not init_file.exists():
                        doc_title = dir_path.name.replace("_", " ").title()
                        content = f'"""EAOS {doc_title} Package."""\n'
                        init_file.write_text(content, encoding="utf-8")
                        count += 1
        return count

    def _ensure_package_readmes(self) -> int:
        """Ensure top-level packages have README.md documentation."""
        count = 0
        packages_dir = self.root / "packages"
        if not packages_dir.exists():
            return 0

        for pkg in packages_dir.iterdir():
            if not pkg.is_dir() or pkg.name in {"__pycache__", ".venv"}:
                continue
            readme = pkg / "README.md"
            if not readme.exists():
                pkg_title = pkg.name.replace("_", " ").title()
                content = (
                    f"# EAOS {pkg_title} Package\n\n"
                    f"## Overview\n"
                    f"Architecture capability package for {pkg_title}.\n\n"
                    f"## Structure\n"
                    f"- `domain/`: Domain entities and value objects\n"
                    f"- `ports/`: Protocol interface boundaries\n"
                    f"- `adapters/`: Infrastructure implementation\n"
                )
                readme.write_text(content, encoding="utf-8")
                count += 1
        return count

    def _ensure_app_configs(self) -> int:
        """Ensure applications have pyproject.toml and README.md."""
        count = 0
        apps_dir = self.root / "apps"
        if not apps_dir.exists():
            return 0

        for app in apps_dir.iterdir():
            if not app.is_dir() or app.name in {"__pycache__", ".venv"}:
                continue

            app_readme = app / "README.md"
            if not app_readme.exists():
                app_title = app.name.replace("_", " ").title()
                content = f"# EAOS {app_title} Application\n\nExecutable application layer for {app_title}.\n"
                app_readme.write_text(content, encoding="utf-8")
                count += 1

            app_config = app / "pyproject.toml"
            if not app_config.exists() and app.name != "api":
                app_title = app.name.replace("_", "-")
                content = (
                    f'[project]\nname = "eaos-{app_title}"\n'
                    f'version = "0.1.0"\n'
                    f'description = "EAOS {app_title} application"\n'
                )
                app_config.write_text(content, encoding="utf-8")
                count += 1

        return count


if __name__ == "__main__":
    scanner = PackageRepositoryScanner()
    res = scanner.scan_and_provision()
    print(f"Package Scan Complete: {res}")
