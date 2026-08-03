"""
Missing Type Annotation Detector.

This module inspects Python source code (as text) and reports every
function or method definition that is missing at least one required
type annotation (a parameter annotation or the return annotation).

Only the standard library (``ast``) is used; no external data is
executed or evaluated -- the source is only parsed into an AST, never
run.
"""

from __future__ import annotations

import ast
from typing import List, Optional, Tuple


def _first_positional_index_is_exempt(
    arg: ast.arg, is_method: bool
) -> bool:
    """Return True if this argument is the exempt self/cls parameter."""
    return is_method and arg.arg in ("self", "cls")


def _function_is_untyped(node: ast.AST, is_method: bool) -> bool:
    """Return True if the given function/async function node has at
    least one missing required annotation."""
    args = node.args  # type: ignore[attr-defined]

    positional_params: List[ast.arg] = list(args.posonlyargs) + list(args.args)

    for index, param in enumerate(positional_params):
        if index == 0 and _first_positional_index_is_exempt(param, is_method):
            continue
        if param.annotation is None:
            return True

    for param in args.kwonlyargs:
        if param.annotation is None:
            return True

    if args.vararg is not None and args.vararg.annotation is None:
        return True

    if args.kwarg is not None and args.kwarg.annotation is None:
        return True

    if node.returns is None:  # type: ignore[attr-defined]
        return True

    return False


class _AnnotationVisitor(ast.NodeVisitor):
    """Walks the AST tracking whether the current function is a direct
    method of a class (i.e. its immediate parent scope is a class
    body) versus a module-level or nested function."""

    def __init__(self) -> None:
        self.results: List[Tuple[str, int]] = []
        # Stack of markers describing enclosing scopes: 'class' or 'func'
        self._scope_stack: List[str] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._scope_stack.append("class")
        self.generic_visit(node)
        self._scope_stack.pop()

    def _visit_function(self, node: ast.AST) -> None:
        is_method = bool(self._scope_stack) and self._scope_stack[-1] == "class"

        if _function_is_untyped(node, is_method):
            self.results.append((node.name, node.lineno))  # type: ignore[attr-defined]

        self._scope_stack.append("func")
        self.generic_visit(node)
        self._scope_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_function(node)

    # Lambdas are intentionally not visited/reported; generic_visit
    # will still walk into them (e.g. for nested defs inside default
    # values), but we never treat a Lambda itself as reportable.


def find_untyped_functions(source: str) -> List[Tuple[str, int]]:
    """Parse ``source`` and return a list of (function_name, lineno)
    tuples for every function/method definition missing at least one
    required type annotation.

    Args:
        source: Python source code as a string.

    Returns:
        A list of (name, lineno) tuples sorted ascending by
        (lineno, name).

    Raises:
        ValueError: if ``source`` is not a string, or is not valid
            Python source (i.e. ``ast.parse`` fails).
    """
    if not isinstance(source, str):
        raise ValueError("source must be a string")

    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError("source is not valid Python") from exc
    except (ValueError, TypeError) as exc:
        # Defensive: ast.parse can also raise ValueError for null
        # bytes etc. Wrap uniformly without leaking internals.
        raise ValueError("source is not valid Python") from exc

    visitor = _AnnotationVisitor()
    visitor.visit(tree)

    return sorted(visitor.results, key=lambda item: (item[1], item[0]))
