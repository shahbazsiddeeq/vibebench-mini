"""Utilities for analyzing Python source code."""

from __future__ import annotations

import ast
import re


_SNAKE_CASE_NAME = re.compile(r"[a-z_][a-z0-9_]*\Z")


def non_snake_case_functions(source: str) -> list[str]:
    """Return function names that do not follow lowercase snake_case.

    Both synchronous and asynchronous definitions are considered, including
    nested functions and methods. Results are ordered by source location.

    Raises:
        TypeError: If ``source`` is not a string.
        ValueError: If ``source`` contains invalid Python syntax.
    """
    if not isinstance(source, str):
        raise TypeError("source must be a string")

    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError) as exc:
        raise ValueError("source contains invalid Python syntax") from None

    definitions: list[tuple[int, int, str]] = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if _SNAKE_CASE_NAME.fullmatch(node.name) is None:
                definitions.append((node.lineno, node.col_offset, node.name))

    definitions.sort(key=lambda item: (item[0], item[1]))
    return [name for _, _, name in definitions]
