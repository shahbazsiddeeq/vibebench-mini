from __future__ import annotations

import ast


def docstring_coverage(source: str) -> float:
    """Return the fraction of function/class definitions that have a docstring.

    Considers FunctionDef, AsyncFunctionDef and ClassDef nodes. If there are no
    such definitions, returns 1.0. Raises ValueError on a syntax error.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError("source is not valid Python") from exc

    definitions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    ]
    if not definitions:
        return 1.0

    documented = sum(1 for node in definitions if ast.get_docstring(node) is not None)
    return documented / len(definitions)
