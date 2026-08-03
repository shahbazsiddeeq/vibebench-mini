from __future__ import annotations

import ast
import re

_SNAKE_CASE = re.compile(r"^[a-z_][a-z0-9_]*$")


def non_snake_case_functions(source: str) -> list[str]:
    """Return names of function definitions that are not snake_case.

    Includes top-level and nested (Async)FunctionDef nodes, in source order.
    Raises ValueError on a syntax error.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError("source is not valid Python") from exc

    funcs = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    funcs.sort(key=lambda n: (n.lineno, n.col_offset))
    return [f.name for f in funcs if not _SNAKE_CASE.match(f.name)]
