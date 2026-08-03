"""Detect imported names that are never referenced in Python source."""

from __future__ import annotations

import ast


def unused_imports(source: str) -> list[str]:
    """Return imported bound names that do not appear elsewhere as ``ast.Name``.

    Names are returned in source order. Star imports are ignored.

    Args:
        source: Python source code to inspect.

    Raises:
        TypeError: If ``source`` is not a string.
        ValueError: If ``source`` contains invalid Python syntax.
    """
    if not isinstance(source, str):
        raise TypeError("source must be a string")

    try:
        tree = ast.parse(source, mode="exec")
    except (SyntaxError, ValueError, TypeError):
        raise ValueError("invalid Python source") from None

    imported_names: list[str] = []
    referenced_names: set[str] = set()

    class ImportVisitor(ast.NodeVisitor):
        def visit_Import(self, node: ast.Import) -> None:
            for alias in node.names:
                bound_name = alias.asname or alias.name.split(".", 1)[0]
                imported_names.append(bound_name)

        def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
            for alias in node.names:
                if alias.name != "*":
                    imported_names.append(alias.asname or alias.name)

        def visit_Name(self, node: ast.Name) -> None:
            referenced_names.add(node.id)

    ImportVisitor().visit(tree)
    return [name for name in imported_names if name not in referenced_names]
