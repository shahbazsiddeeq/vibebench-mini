from __future__ import annotations

import ast

_EXEMPT = {"self", "cls"}


def _parse(source: str) -> ast.Module:
    try:
        return ast.parse(source)
    except SyntaxError as exc:
        raise ValueError(f"invalid Python source: {exc}") from exc


def find_untyped_functions(source: str) -> list[tuple[str, int]]:
    tree = _parse(source)

    # Identify functions that are methods: defined directly in a class body.
    method_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for stmt in node.body:
                if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    method_ids.add(id(stmt))

    results: list[tuple[str, int]] = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        a = node.args
        params = list(a.posonlyargs) + list(a.args) + list(a.kwonlyargs)
        if a.vararg is not None:
            params.append(a.vararg)
        if a.kwarg is not None:
            params.append(a.kwarg)

        positional = a.posonlyargs + a.args
        exempt = None
        if id(node) in method_ids and positional and positional[0].arg in _EXEMPT:
            exempt = positional[0]

        missing = node.returns is None
        if not missing:
            for p in params:
                if p is exempt:
                    continue
                if p.annotation is None:
                    missing = True
                    break

        if missing:
            results.append((node.name, node.lineno))

    results.sort(key=lambda t: (t[1], t[0]))
    return results
