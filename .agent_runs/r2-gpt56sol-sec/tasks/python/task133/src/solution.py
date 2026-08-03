"""Utilities for measuring docstring coverage in Python source code."""

import ast


def docstring_coverage(source: str) -> float:
    """Return the fraction of function and class definitions with docstrings.

    Both synchronous and asynchronous functions are included, as are nested
    definitions. If no definitions exist, ``1.0`` is returned.

    Args:
        source: Python source code to inspect.

    Raises:
        TypeError: If ``source`` is not a string.
        ValueError: If ``source`` contains invalid Python syntax.
    """
    if not isinstance(source, str):
        raise TypeError("source must be a string")

    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError, TypeError) as exc:
        raise ValueError("source contains invalid Python syntax") from exc

    definitions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    ]

    if not definitions:
        return 1.0

    documented = sum(ast.get_docstring(node, clean=False) is not None for node in definitions)
    return documented / len(definitions)
