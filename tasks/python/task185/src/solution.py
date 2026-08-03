from __future__ import annotations

import ast


def _parse(source: str) -> ast.Module:
    try:
        return ast.parse(source)
    except SyntaxError as exc:
        raise ValueError(f"invalid Python source: {exc}") from exc


def find_mutable_defaults(source: str) -> list[tuple[str, int]]:
    """Return (function_name, lineno) for functions with mutable-literal defaults.

    A default is "mutable" iff its AST node is a list, dict, or set display.
    """
    tree = _parse(source)

    results: list[tuple[str, int]] = []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        args = node.args
        defaults = list(args.defaults) + [d for d in args.kw_defaults if d is not None]
        if any(isinstance(d, (ast.List, ast.Dict, ast.Set)) for d in defaults):
            results.append((node.name, node.lineno))

    results.sort(key=lambda t: (t[1], t[0]))
    return results
