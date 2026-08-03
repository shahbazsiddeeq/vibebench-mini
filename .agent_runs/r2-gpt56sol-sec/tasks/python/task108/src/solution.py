"""Utilities for estimating basic Python function complexity."""

from __future__ import annotations

import ast


def estimate_complexity(func_source: str) -> dict[str, int]:
    """Estimate line, branch, and return counts for one top-level function.

    Raises:
        ValueError: If the input is empty, invalid Python, or does not contain
            exactly one top-level function definition.
    """
    if not isinstance(func_source, str) or not func_source.strip():
        raise ValueError("source must be a non-empty string")

    lines = sum(1 for line in func_source.splitlines() if line.strip())

    try:
        tree = ast.parse(func_source)
    except (SyntaxError, ValueError, TypeError, RecursionError) as exc:
        raise ValueError("source could not be parsed") from None

    function_types = (ast.FunctionDef, ast.AsyncFunctionDef)
    top_level_functions = [
        node for node in tree.body if isinstance(node, function_types)
    ]
    if len(top_level_functions) != 1:
        raise ValueError("source must define exactly one top-level function")

    branches = 0
    returns = 0
    branch_types = (ast.If, ast.For, ast.While, ast.ExceptHandler)

    for node in ast.walk(top_level_functions[0]):
        if isinstance(node, branch_types):
            branches += 1
        elif isinstance(node, ast.Return):
            returns += 1

    return {"lines": lines, "branches": branches, "returns": returns}
