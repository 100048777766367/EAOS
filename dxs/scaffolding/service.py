from __future__ import annotations

from pathlib import Path

from dxs.contracts.scaffolding import ScaffoldResult


def scaffold_capability(
    root: Path,
    name: str,
) -> ScaffoldResult:
    target = root / name

    created: list[Path] = []
    skipped: list[Path] = []

    for relative in (
        "domain/__init__.py",
        "application/__init__.py",
        "ports/__init__.py",
        "adapters/__init__.py",
        "tests/__init__.py",
        "README.md",
    ):
        path = target / relative

        if path.exists():
            skipped.append(path)
            continue

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        content = (
            f"# {name}\n\nArchitecture-aware capability scaffold.\n"
            if path.name == "README.md"
            else '"""Generated package boundary."""\n'
        )

        path.write_text(
            content,
            encoding="utf-8",
        )

        created.append(path)

    return ScaffoldResult(
        target,
        tuple(created),
        tuple(skipped),
    )


class ScaffoldingService:
    """
    Application service wrapper around scaffold capability.
    """

    def scaffold(
        self,
        root: Path,
        name: str,
    ) -> ScaffoldResult:
        return scaffold_capability(
            root=root,
            name=name,
        )


__all__ = [
    "ScaffoldingService",
    "scaffold_capability",
]
