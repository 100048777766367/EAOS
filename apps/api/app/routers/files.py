"""Real file explorer and persistent storage router."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, ConfigDict

router: Final[APIRouter] = APIRouter(
    prefix="/api/files",
    tags=["File Explorer"],
)

ROOT_DIR: Final[Path] = Path(__file__).resolve().parents[4]


class FileContentResponse(BaseModel):
    """File content response."""

    model_config = ConfigDict(frozen=True)

    path: str
    content: str


class SaveFileRequest(BaseModel):
    """Save file request."""

    model_config = ConfigDict(frozen=True)

    path: str
    content: str


def _safe_path(relative_path: str) -> Path:
    """Resolve a path inside the workspace."""
    clean_path = relative_path.lstrip("/\\")

    try:
        target = (ROOT_DIR / clean_path).resolve()

        target.relative_to(ROOT_DIR.resolve())

    except (OSError, ValueError) as exc:
        raise HTTPException(
            status_code=403,
            detail="Access denied: outside workspace.",
        ) from exc

    return target


@router.get(
    "/content",
    response_model=FileContentResponse,
)
async def get_file_content(
    path: str = Query(
        ...,
        description="Workspace-relative file path.",
    ),
) -> FileContentResponse:
    """Read a workspace file."""
    file_path = _safe_path(path)

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"File not found: {path}",
        )

    try:
        content = file_path.read_text(
            encoding="utf-8",
            errors="replace",
        )

    except OSError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to read file: {exc!s}",
        ) from exc

    return FileContentResponse(
        path=path,
        content=content,
    )


@router.post("/save")
async def save_file_content(
    payload: SaveFileRequest,
) -> dict[str, Any]:
    """Persist a file inside the workspace."""
    file_path = _safe_path(payload.path)

    try:
        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path.write_text(
            payload.content,
            encoding="utf-8",
        )

    except OSError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {exc!s}",
        ) from exc

    return {
        "status": "SUCCESS",
        "message": (f"File '{payload.path}' saved to disk."),
    }


@router.get("/tree")
async def get_directory_tree(
    dir_path: str | None = None,
) -> list[dict[str, Any]]:
    """Return one workspace directory level."""
    target = _safe_path(dir_path) if dir_path else ROOT_DIR.resolve()

    if not target.exists() or not target.is_dir():
        raise HTTPException(
            status_code=400,
            detail="Invalid directory path.",
        )

    ignore_dirs = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        ".idea",
        ".vscode",
        "node_modules",
    }

    try:
        items = sorted(
            target.iterdir(),
            key=lambda item: (
                not item.is_dir(),
                item.name.lower(),
            ),
        )

        tree: list[dict[str, Any]] = []

        for item in items:
            if item.is_dir() and item.name in ignore_dirs:
                continue

            relative = item.relative_to(ROOT_DIR)

            tree.append(
                {
                    "name": item.name,
                    "path": str(relative).replace(
                        "\\",
                        "/",
                    ),
                    "type": ("directory" if item.is_dir() else "file"),
                    "extension": (item.suffix.lstrip(".") if item.is_file() else None),
                }
            )

        return tree

    except OSError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to scan tree: {exc!s}",
        ) from exc
