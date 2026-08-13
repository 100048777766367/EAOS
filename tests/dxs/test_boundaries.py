from pathlib import Path

SUBSYSTEMS = (
    "cli",
    "doctor",
    "bootstrap",
    "scaffolding",
    "debugging",
    "testing",
    "validation",
    "diagnostics",
    "workspace",
    "ide",
    "documentation",
    "ai",
    "templates",
    "integrations",
)


def test_all_dxs_subsystems_exist() -> None:
    root = Path(__file__).parents[2] / "dxs"
    for subsystem in SUBSYSTEMS:
        assert (root / subsystem / "__init__.py").exists()
        assert (root / subsystem / "README.md").exists()
