"""Splay Tree API router."""

from __future__ import annotations

import structlog
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

logger = structlog.get_logger()

router = APIRouter(
    prefix="/splay",
    tags=["Splay Operations"],
)


class SplayRequest(BaseModel):
    """Splay operation request."""

    model_config = ConfigDict(frozen=True)

    keys: list[int] = Field(
        default_factory=list,
        description="Initial tree keys.",
    )

    operation: str = Field(
        default="insert",
        description="insert or search.",
    )

    target: int | None = Field(
        default=None,
        description="Target key.",
    )


class SplayResponse(BaseModel):
    """Splay operation response."""

    model_config = ConfigDict(frozen=True)

    success: bool
    root: int | None = None
    traversal: list[int] = Field(default_factory=list)
    message: str


class SplayTreeNode:
    """Node of a Splay Tree."""

    def __init__(self, key: int) -> None:
        self.key = key
        self.left: SplayTreeNode | None = None
        self.right: SplayTreeNode | None = None


class SplayTree:
    """Basic Splay Tree implementation."""

    def __init__(self) -> None:
        self.root: SplayTreeNode | None = None

    def _right_rotate(
        self,
        x: SplayTreeNode,
    ) -> SplayTreeNode:
        y = x.left

        if y is None:
            return x

        x.left = y.right
        y.right = x

        return y

    def _left_rotate(
        self,
        x: SplayTreeNode,
    ) -> SplayTreeNode:
        y = x.right

        if y is None:
            return x

        x.right = y.left
        y.left = x

        return y

    def _splay(
        self,
        root: SplayTreeNode | None,
        key: int,
    ) -> SplayTreeNode | None:
        if root is None or root.key == key:
            return root

        if key < root.key:
            left = root.left

            if left is None:
                return root

            if key < left.key:
                left.left = self._splay(
                    left.left,
                    key,
                )
                root = self._right_rotate(root)

            elif key > left.key:
                left.right = self._splay(
                    left.right,
                    key,
                )

                if left.right is not None:
                    root.left = self._left_rotate(left)

            return self._right_rotate(root) if root.left is not None else root

        right = root.right

        if right is None:
            return root

        if key > right.key:
            right.right = self._splay(
                right.right,
                key,
            )
            root = self._left_rotate(root)

        elif key < right.key:
            right.left = self._splay(
                right.left,
                key,
            )

            if right.left is not None:
                root.right = self._right_rotate(right)

        return self._left_rotate(root) if root.right is not None else root

    def insert(self, key: int) -> None:
        """Insert a key."""
        if self.root is None:
            self.root = SplayTreeNode(key)
            return

        self.root = self._splay(
            self.root,
            key,
        )

        if self.root is None:
            self.root = SplayTreeNode(key)
            return

        if self.root.key == key:
            return

        node = SplayTreeNode(key)

        if key < self.root.key:
            node.right = self.root
            node.left = self.root.left
            self.root.left = None

        else:
            node.left = self.root
            node.right = self.root.right
            self.root.right = None

        self.root = node

    def search(self, key: int) -> bool:
        """Search for a key and splay it."""
        self.root = self._splay(
            self.root,
            key,
        )

        return self.root is not None and self.root.key == key

    def inorder(self) -> list[int]:
        """Return sorted tree traversal."""
        result: list[int] = []

        def traverse(
            node: SplayTreeNode | None,
        ) -> None:
            if node is None:
                return

            traverse(node.left)
            result.append(node.key)
            traverse(node.right)

        traverse(self.root)

        return result


@router.post(
    "/",
    response_model=SplayResponse,
    status_code=status.HTTP_200_OK,
)
async def process_splay_operation(
    payload: SplayRequest,
) -> SplayResponse:
    """Execute a Splay Tree operation."""
    try:
        tree = SplayTree()

        for key in payload.keys:
            tree.insert(key)

        message = "Splay Tree initialized successfully."

        if payload.operation == "search" and payload.target is not None:
            found = tree.search(payload.target)

            message = f"Key {payload.target} found." if found else f"Key {payload.target} not found."

        elif payload.operation == "insert" and payload.target is not None:
            tree.insert(payload.target)

            message = f"Key {payload.target} inserted."

        elif payload.operation not in {
            "insert",
            "search",
        }:
            raise HTTPException(
                status_code=400,
                detail="Operation must be 'insert' or 'search'.",
            )

        return SplayResponse(
            success=True,
            root=(tree.root.key if tree.root is not None else None),
            traversal=tree.inorder(),
            message=message,
        )

    except HTTPException:
        raise

    except Exception as exc:
        logger.error(
            "splay_operation_error",
            error=str(exc),
        )

        raise HTTPException(
            status_code=500,
            detail=f"Splay operation failed: {exc!s}",
        ) from exc
