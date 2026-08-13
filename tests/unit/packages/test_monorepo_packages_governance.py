from __future__ import annotations

from pathlib import Path

from packages.package_registry import MonorepoPackageRegistryEngine

"""Unit tests for packages/ monorepo governance scanner."""


def test_monorepo_package_registry_audit(tmp_path: Path) -> None:
    """Test auditing monorepo package structure."""
    pkg_dir = tmp_path / "packages" / "sample_capability"
    pkg_dir.mkdir(parents=True, exist_ok=True)
    (pkg_dir / "README.md").write_text("# Sample Package")
    (pkg_dir / "__init__.py").write_text('"""Sample."""')

    sub_dir = pkg_dir / "domain"
    sub_dir.mkdir(parents=True, exist_ok=True)
    (sub_dir / "__init__.py").write_text('"""Domain."""')

    engine = MonorepoPackageRegistryEngine(workspace_root=tmp_path)
    specs = engine.audit_all_packages()

    assert len(specs) == 1
    assert specs[0].package_name == "sample_capability"
    assert specs[0].is_compliant is True
