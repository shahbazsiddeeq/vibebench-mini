from __future__ import annotations

import ast


class _FunctionCollector(ast.NodeVisitor):
    """Collect all function and async-function definitions."""

    def __init__(self) -> None:
        self.functions: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.functions.append(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.functions.append(node)
        self.generic_visit(node)


class _ComplexityCounter(ast.NodeVisitor):
    """Count decision points while respecting nested-scope boundaries."""

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

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        self.complexity += max(0, len(node.values) - 1)
        self.generic_visit(node)

    def visit_comprehension(self, node: ast.comprehension) -> None:
        self.complexity += len(node.ifs)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        # Nested function bodies belong to their own complexity calculation.
        return None

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        return None

    def visit_Lambda(self, node: ast.Lambda) -> None:
        return None

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        return None


def compute_complexity(source: str) -> list[tuple[str, int, int]]:
    """Return cyclomatic complexity information for every function in source."""
    if not isinstance(source, str):
        raise TypeError("source must be a string")

    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        raise ValueError("source is not valid Python") from None

    collector = _FunctionCollector()
    collector.visit(tree)

    results: list[tuple[str, int, int]] = []
    for function in collector.functions:
        counter = _ComplexityCounter()
        for statement in function.body:
            counter.visit(statement)
        results.append((function.name, function.lineno, counter.complexity))

    results.sort(key=lambda item: (item[1], item[0]))
    return results
