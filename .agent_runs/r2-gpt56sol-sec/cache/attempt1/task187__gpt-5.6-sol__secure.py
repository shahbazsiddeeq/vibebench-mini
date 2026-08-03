"""Utilities for detecting bare exception handlers in Python source code."""

from __future__ import annotations

import ast


def find_bare_excepts(source: str) -> list[int]:
    """Return line numbers of all bare ``except:`` clauses in *source*.

    Args:
        source: Python source code to inspect.

    Raises:
        TypeError: If *source* is not a string.
        ValueError: If *source* is not valid Python syntax.
    """
    if not isinstance(source, str):
        raise TypeError("source must be a string")

    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("source is not valid Python") from None

    lines = [
        node.lineno
        for node in ast.walk(tree)
        if isinstance(node, ast.ExceptHandler) and node.type is None
    ]
    return sorted(lines)
