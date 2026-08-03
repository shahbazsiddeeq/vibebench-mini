"""
Code Complexity Estimator
--------------------------

Provides `estimate_complexity(func_source: str) -> dict`, which parses the
source code of a single Python function definition and returns basic
complexity metrics: number of non-blank lines, number of branch nodes, and
number of return statements.

This module only uses the standard library and never uses eval/exec on the
supplied source; it relies exclusively on `ast.parse` for safe static
analysis.
"""

import ast
from typing import Dict


def estimate_complexity(func_source: str) -> Dict[str, int]:
    """
    Parse `func_source` (expected to contain exactly one top-level function
    definition) and return a dict with keys:
      - "lines": number of non-blank lines in the source text
      - "branches": count of ast.If, ast.For, ast.While, ast.ExceptHandler
        nodes anywhere in the function body
      - "returns": count of ast.Return nodes anywhere in the function body

    Raises:
        ValueError: if the source is empty/whitespace only, cannot be
            parsed as valid Python, or does not define exactly one
            top-level function.
    """
    if not isinstance(func_source, str):
        raise ValueError("func_source must be a string")

    if not func_source.strip():
        raise ValueError("func_source is empty")

    try:
        tree = ast.parse(func_source, mode="exec")
    except (SyntaxError, ValueError):
        raise ValueError("func_source could not be parsed as valid Python")
    except Exception:
        # Catch-all to avoid leaking internal parser details/exceptions.
        raise ValueError("func_source could not be parsed as valid Python")

    top_level_nodes = list(tree.body)

    if len(top_level_nodes) != 1:
        raise ValueError("func_source must define exactly one top-level function")

    (func_node,) = top_level_nodes

    if not isinstance(func_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        raise ValueError("func_source must define exactly one top-level function")

    # Count non-blank lines in the raw source text.
    lines = [line for line in func_source.splitlines() if line.strip()]
    line_count = len(lines)

    branch_count = 0
    return_count = 0

    for node in ast.walk(func_node):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
            branch_count += 1
        elif isinstance(node, ast.Return):
            return_count += 1

    return {
        "lines": line_count,
        "branches": branch_count,
        "returns": return_count,
    }
