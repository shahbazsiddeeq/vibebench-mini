"""
Mutable Default Argument Detector.

Provides `find_mutable_defaults`, which statically analyzes Python source
code (via the `ast` module, never `eval`/`exec`) to find function
definitions that use a mutable literal display (list/dict/set) as a
default argument value.
"""

import ast


def _is_mutable_literal(node: ast.AST) -> bool:
    """Return True if node is a list, dict, or set display."""
    return isinstance(node, (ast.List, ast.Dict, ast.Set))


def _function_has_mutable_default(func: ast.AST) -> bool:
    """Check whether a function/async function node has a mutable default."""
    args = func.args

    # Positional/regular defaults (defaults for the trailing args in
    # posonlyargs + args), and keyword-only defaults.
    for default in args.defaults:
        if default is not None and _is_mutable_literal(default):
            return True

    for default in args.kw_defaults:
        if default is not None and _is_mutable_literal(default):
            return True

    return False


def find_mutable_defaults(source: str) -> list[tuple[str, int]]:
    """
    Parse `source` and return a sorted list of (function_name, lineno)
    tuples for every function definition (including methods and nested
    functions, both `def` and `async def`) that has at least one
    parameter whose default value is a mutable literal display
    ([...] / {...} / {1, 2}).

    Lambdas are ignored. Tuple defaults, constants, and calls like
    list()/dict() do not count.

    Raises:
        ValueError: if `source` is not valid Python source.
    """
    if not isinstance(source, str):
        raise ValueError("source must be a string")

    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python source: {exc}") from None
    except ValueError as exc:
        # e.g. null bytes in source
        raise ValueError(f"Invalid Python source: {exc}") from None

    results: list[tuple[str, int]] = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if _function_has_mutable_default(node):
                results.append((node.name, node.lineno))

    results.sort(key=lambda item: (item[1], item[0]))
    return results
