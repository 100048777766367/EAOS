"""Architecture rules enforcement test suite."""

from pathlib import Path


def test_domain_layer_has_no_infrastructure_imports() -> None:
    """Verify Domain layer does not import infrastructure packages."""
    packages_dir = Path("packages")
    if not packages_dir.exists():
        return

    forbidden = ["fastapi", "sqlalchemy", "redis", "docker"]
    for py_file in packages_dir.rglob("domain/**/*.py"):
        content = py_file.read_text(encoding="utf-8")
        for pkg in forbidden:
            assert f"import {pkg}" not in content, f"Domain file {py_file} contains forbidden import: {pkg}"
