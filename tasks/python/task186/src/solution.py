from __future__ import annotations

import ast


def _parse(source: str) -> ast.Module:
    try:
        return ast.parse(source)
    except SyntaxError as exc:
        raise ValueError(f"invalid Python source: {exc}") from exc


def _complexity_of(func: ast.AST) -> int:
    """Cyclomatic complexity of a function's own body (nested scopes excluded)."""
    total = 1

    def visit(node: ast.AST) -> None:
        nonlocal total
        # Do not descend into nested scopes; they are measured separately.
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.Lambda, ast.ClassDef)):
            return
        if isinstance(node, (ast.If, ast.For, ast.AsyncFor, ast.While,
                             ast.ExceptHandler, ast.IfExp)):
            total += 1
        elif isinstance(node, ast.BoolOp):
            total += len(node.values) - 1
        elif isinstance(node, ast.comprehension):
            total += len(node.ifs)
        for child in ast.iter_child_nodes(node):
            visit(child)

    for stmt in func.body:  # type: ignore[attr-defined]
        visit(stmt)
    return total


def compute_complexity(source: str) -> list[tuple[str, int, int]]:
    tree = _parse(source)
    results: list[tuple[str, int, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            results.append((node.name, node.lineno, _complexity_of(node)))
    results.sort(key=lambda t: (t[1], t[0]))
    return results
