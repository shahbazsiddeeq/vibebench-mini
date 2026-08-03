"""Detect function definitions with missing type annotations."""

from __future__ import annotations

import ast


def find_untyped_functions(source: str) -> list[tuple[str, int]]:
    """Return names and line numbers of functions missing required annotations.

    A direct class-body method may omit the annotation on its first positional
    parameter when that parameter is named exactly ``self`` or ``cls``.

    Raises:
        TypeError: If *source* is not a string.
        ValueError: If *source* is not valid Python.
    """
    if not isinstance(source, str):
        raise TypeError("source must be a string")

    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("source is not valid Python") from None

    direct_methods: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for statement in node.body:
                if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    direct_methods.add(id(statement))

    results: list[tuple[str, int]] = []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        missing_annotation = node.returns is None
        positional_parameters = [
            *node.args.posonlyargs,
            *node.args.args,
        ]

        for index, parameter in enumerate(positional_parameters):
            exempt = (
                id(node) in direct_methods
                and index == 0
                and parameter.arg in {"self", "cls"}
            )
            if parameter.annotation is None and not exempt:
                missing_annotation = True

        for parameter in node.args.kwonlyargs:
            if parameter.annotation is None:
                missing_annotation = True

        if node.args.vararg is not None and node.args.vararg.annotation is None:
            missing_annotation = True

        if node.args.kwarg is not None and node.args.kwarg.annotation is None:
            missing_annotation = True

        if missing_annotation:
            results.append((node.name, node.lineno))

    return sorted(results, key=lambda item: (item[1], item[0]))
