from __future__ import annotations

import ast


def unused_imports(source: str) -> list[str]:
    """Return bound import names that are never referenced as a Name.

    For 'import x as y' or 'from m import a as b' the bound name is the alias
    (y, b); for 'import a.b.c' the bound name is the top package 'a'. Results
    are in source order. Raises ValueError on a syntax error.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError("source is not valid Python") from exc

    used: set[str] = {
        node.id for node in ast.walk(tree) if isinstance(node, ast.Name)
    }

    bound: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname or alias.name.split(".")[0]
                bound.append((node.lineno, node.col_offset, name))
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                # A star import ('from m import *') binds no inspectable name;
                # it never appears as a bound, unused name.
                if alias.name == "*":
                    continue
                name = alias.asname or alias.name
                bound.append((node.lineno, node.col_offset, name))

    bound.sort(key=lambda item: (item[0], item[1]))
    return [name for _, _, name in bound if name not in used]
