"""
src/solution.py

Cyclomatic Complexity Analyzer.

Provides `compute_complexity(source: str) -> list[tuple[str, int, int]]`
which parses Python source code and computes a McCabe-style cyclomatic
complexity for every function definition (including methods and nested
functions), measured strictly over that function's own body (excluding
nested defs/async defs/lambdas/classes, which are reported separately or
not at all in the case of lambdas).
"""

import ast


def _local_complexity(func_node):
    """Compute cyclomatic complexity contributed by a function's own body,
    not descending into nested function/async function/lambda/class defs.
    """
    complexity = 1  # base complexity

    def visit(node):
        nonlocal complexity

        # Do not descend into nested scopes; they are measured separately
        # (or, in the case of lambdas, not reported at all).
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                              ast.Lambda, ast.ClassDef)):
            return

        if isinstance(node, ast.If):
            complexity += 1
        elif isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
            complexity += 1
        elif isinstance(node, ast.ExceptHandler):
            complexity += 1
        elif isinstance(node, ast.IfExp):
            complexity += 1
        elif isinstance(node, ast.comprehension):
            complexity += len(node.ifs)
        elif isinstance(node, ast.BoolOp):
            complexity += max(len(node.values) - 1, 0)

        for child in ast.iter_child_nodes(node):
            visit(child)

    for stmt in func_node.body:
        visit(stmt)

    return complexity


def compute_complexity(source: str):
    """Parse `source` and return a sorted list of
    (function_name, lineno, complexity) tuples for every function
    definition (def / async def) found anywhere in the source, including
    nested functions and methods. Lambdas are never reported.

    Raises ValueError if `source` is not valid Python.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python source: {exc}") from exc

    results = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = node.name
            lineno = node.lineno
            complexity = _local_complexity(node)
            results.append((name, lineno, complexity))

    results.sort(key=lambda t: (t[1], t[0]))
    return results
