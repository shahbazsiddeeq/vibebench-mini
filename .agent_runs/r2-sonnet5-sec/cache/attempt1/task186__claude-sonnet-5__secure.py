"""
Cyclomatic Complexity Analyzer.

This module exposes a single public function, `compute_complexity`, which
parses a string containing Python source code (using the standard library
`ast` module only -- no `eval`/`exec` and no execution of the supplied
source) and computes a simple McCabe-style cyclomatic complexity for every
function definition found in it.

Security notes:
    * The source string is only ever parsed with `ast.parse`; it is never
      executed, compiled to bytecode, or passed to `eval`/`exec`.
    * Input validation is performed on the type of the argument.
    * Any parsing failure (SyntaxError, ValueError from ast itself, etc.)
      is converted into a `ValueError` with a generic message so that
      internal details (e.g. file paths, interpreter internals) are never
      leaked to callers.
"""

from __future__ import annotations

import ast
from typing import List, Tuple

__all__ = ["compute_complexity"]

# Node types that introduce a new, independently-measured scope.  When we
# encounter one of these while walking a function's body we must NOT
# descend into it -- it is reported as its own separate entry (or, in the
# case of lambdas/classes, not reported as a function at all, but its
# internals still must not pollute the enclosing function's complexity).
_SCOPE_BOUNDARY_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)

# Node types that represent loops for complexity purposes.
_LOOP_TYPES = (ast.For, ast.AsyncFor, ast.While)


def _complexity_of(func_node: ast.AST) -> int:
    """Compute the cyclomatic complexity of a single function's own body.

    Nested function/async function/lambda/class definitions are treated as
    opaque boundaries: their internals are not traversed at all when
    computing the complexity of the enclosing function.
    """
    complexity = 1  # base complexity

    def visit(node: ast.AST) -> None:
        nonlocal complexity
        for child in ast.iter_child_nodes(node):
            if isinstance(child, _SCOPE_BOUNDARY_TYPES):
                # Do not recurse into nested scopes at all.
                continue

            if isinstance(child, ast.If):
                complexity += 1
            elif isinstance(child, _LOOP_TYPES):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.IfExp):
                complexity += 1
            elif isinstance(child, ast.comprehension):
                complexity += len(child.ifs)
            elif isinstance(child, ast.BoolOp):
                # `and` / `or` with N operands contribute N - 1.
                complexity += max(len(child.values) - 1, 0)

            visit(child)

    visit(func_node)
    return complexity


def compute_complexity(source: str) -> List[Tuple[str, int, int]]:
    """Parse `source` and return cyclomatic complexity info per function.

    Args:
        source: A string containing Python source code.

    Returns:
        A list of (function_name, lineno, complexity) tuples, one for each
        `def`/`async def` found anywhere in the source (including nested
        functions and methods), sorted ascending by (lineno, function_name).

    Raises:
        ValueError: If `source` is not a string, or is not valid Python
            source code.
    """
    if not isinstance(source, str):
        raise ValueError("source must be a string")

    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError, RecursionError):
        # Do not leak internal exception details; raise a clean ValueError.
        raise ValueError("invalid Python source")
    except Exception:
        # Defensive catch-all: never let unexpected internal errors escape
        # with potentially sensitive details.
        raise ValueError("invalid Python source")

    results: List[Tuple[str, int, int]] = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = node.name
            lineno = node.lineno
            complexity = _complexity_of(node)
            results.append((name, lineno, complexity))

    results.sort(key=lambda item: (item[1], item[0]))
    return results
