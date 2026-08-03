"""Cyclomatic complexity analysis for Python functions."""

from __future__ import annotations

import ast


class _ComplexityVisitor(ast.NodeVisitor):
    """Count decision points while excluding nested scopes."""

    def __init__(self) -> None:
        self.complexity = 1

    def visit_If(self, node: ast.If) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_IfExp(self, node: ast.IfExp) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_comprehension(self, node: ast.comprehension) -> None:
        self.complexity += len(node.ifs)
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        self.complexity += max(0, len(node.values) - 1)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        return

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        return

    def visit_Lambda(self, node: ast.Lambda) -> None:
        return

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        return


def compute_complexity(source: str) -> list[tuple[str, int, int]]:
    """Return the cyclomatic complexity of every function in *source*.

    Invalid Python source raises ``ValueError``.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError("source is not valid Python") from exc

    functions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]

    results: list[tuple[str, int, int]] = []
    for function in functions:
        visitor = _ComplexityVisitor()
        for statement in function.body:
            visitor.visit(statement)
        results.append((function.name, function.lineno, visitor.complexity))

    results.sort(key=lambda item: (item[1], item[0]))
    return results
