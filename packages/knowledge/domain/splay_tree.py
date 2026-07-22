from typing import Any


class SplayNode[T]:
    """NÃºt Ä‘áº¡i diá»‡n cho pháº§n tá»­ lÆ°u trong Splay Tree."""

    def __init__(self, key: str, value: T) -> None:
        self.key: str = key  # KhÃ³a tÃ¬m kiáº¿m (vÃ­ dá»¥: artifact_id)
        self.value: T = value  # Dá»¯ liá»‡u Ä‘á»‘i tÆ°á»£ng
        self.left: SplayNode[T] | None = None
        self.right: SplayNode[T] | None = None
        self.parent: SplayNode[T] | None = None


class SplayTree[T]:
    """CÃ¢y Splay Tree tá»± tá»‘i Æ°u hÃ³a."""

    def __init__(self) -> None:
        self.root: SplayNode[T] | None = None

    def _right_rotate(self, x: SplayNode[T]) -> None:
        y = x.left
        if y is None:
            return
        x.left = y.right
        if y.right is not None:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def _left_rotate(self, x: SplayNode[T]) -> None:
        y = x.right
        if y is None:
            return
        x.right = y.left
        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _splay(self, x: SplayNode[T]) -> None:
        """ÄÆ°a nÃºt x vá»«a truy cáº­p lÃªn lÃ m gá»‘c cá»§a cÃ¢y."""
        while x.parent is not None:
            p = x.parent
            g = p.parent
            if g is None:
                # Zig Case
                if x == p.left:
                    self._right_rotate(p)
                else:
                    self._left_rotate(p)
            elif x == p.left and p == g.left:
                # Zig-Zig Case
                self._right_rotate(g)
                self._right_rotate(p)
            elif x == p.right and p == g.right:
                # Zig-Zig Case
                self._left_rotate(g)
                self._left_rotate(p)
            elif x == p.right and p == g.left:
                # Zig-Zag Case
                self._left_rotate(p)
                self._right_rotate(p)
            else:
                # Zig-Zag Case
                self._right_rotate(p)
                self._left_rotate(p)

    def search(self, key: str) -> SplayNode[T] | None:
        """TÃ¬m kiáº¿m khÃ³a vÃ  tá»± Ä‘á»™ng splay nÃºt tÃ¬m tháº¥y lÃªn lÃ m gá»‘c."""
        x = self.root
        while x is not None:
            if key < x.key:
                if x.left is None:
                    self._splay(x)
                    return None
                x = x.left
            elif key > x.key:
                if x.right is None:
                    self._splay(x)
                    return None
                x = x.right
            else:
                self._splay(x)
                return x
        return None

    def insert(self, key: str, value: T) -> None:
        """ChÃ¨n pháº§n tá»­ má»›i vÃ o cÃ¢y nhá»‹ phÃ¢n vÃ  splay lÃªn lÃ m Root."""
        if self.root is None:
            self.root = SplayNode(key, value)
            return

        # Khai bÃ¡o kiá»ƒu tÆ°á»ng minh cho phÃ©p x vÃ  parent nháº­n giÃ¡ trá»‹ None (Sá»­a lá»—i Mypy)
        x: SplayNode[T] | None = self.root
        parent: SplayNode[T] | None = None

        while x is not None:
            parent = x
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                x.value = value
                self._splay(x)
                return

        if parent is None:
            return

        node = SplayNode(key, value)
        node.parent = parent
        if key < parent.key:
            parent.left = node
        else:
            parent.right = node

        self._splay(node)

    def delete(self, key: str) -> bool:
        """XÃ³a pháº§n tá»­ vÃ  splay tÃ¡i sáº¯p xáº¿p láº¡i hai nhÃ¡nh cá»§a cÃ¢y."""
        node = self.search(key)
        if node is None or node.key != key:
            return False

        left_tree = node.left
        right_tree = node.right

        if left_tree:
            left_tree.parent = None
        if right_tree:
            right_tree.parent = None

        if left_tree is None:
            self.root = right_tree
        else:
            max_node = left_tree
            while max_node.right is not None:
                max_node = max_node.right

            self.root = left_tree
            self._splay(max_node)
            self.root.right = right_tree
            if right_tree:
                right_tree.parent = self.root
        return True

    def to_dict(self) -> dict[str, Any] | None:
        def _to_dict(n: SplayNode[T] | None) -> dict[str, Any] | None:
            if n is None:
                return None
            return {
                "key": n.key,
                "left": _to_dict(n.left),
                "right": _to_dict(n.right),
            }

        return _to_dict(self.root)

    def to_mermaid(self) -> str:
        lines = ["graph TD"]

        def _to_mermaid(n: SplayNode[T] | None) -> None:
            if n is None:
                return
            clean_k = n.key.replace("-", "_")
            lines.append(f'    {clean_k}["{n.key}"]')
            if n.left:
                left_k = n.left.key.replace("-", "_")
                lines.append(f"    {clean_k} -->|Left| {left_k}")
                _to_mermaid(n.left)
            if n.right:
                right_k = n.right.key.replace("-", "_")
                lines.append(f"    {clean_k} -->|Right| {right_k}")
                _to_mermaid(n.right)

        _to_mermaid(self.root)
        return "\n".join(lines)
