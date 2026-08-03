"""Utilities for detecting mutable literal defaults in Python source code."""

from __future__ import annotations

import ast

__all__ = ["find_mutable_defaults"]


_MUTABLE_DISPLAYS = (ast.List, ast.Dict, ast.Set)


def find_mutable_defaults(source: str) -> list[tuple[str, int]]:
    """Return functions having list, dict, or set displays as defaults.

    Both regular and keyword-only parameter defaults are inspected. Nested
    functions, methods, and asynchronous functions are included; lambdas are
    ignored.

    Raises:
        TypeError: If ``source`` is not a string.
        ValueError: If ``source`` is not valid Python source code.
    """
    if not isinstance(source, str):
        raise TypeError("source must be a string")

    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        raise ValueError("source is not valid Python") from None

    results: list[tuple[str, int]] = []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        defaults = list(node.args.defaults)
        defaults.extend(
            default for default in node.args.kw_defaults if default is not None
        )

        if any(isinstance(default, _MUTABLE_DISPLAYS) for default in defaults):
            results.append((node.name, node.lineno))

    results.sort(key=lambda item: (item[1], item[0]))
    return results
