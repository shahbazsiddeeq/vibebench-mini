"""Safely evaluate a restricted arithmetic expression."""

from __future__ import annotations

import ast
import operator
from typing import Callable


_BINARY_OPERATORS: dict[type[ast.operator], Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

_UNARY_OPERATORS: dict[type[ast.unaryop], Callable[[float], float]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def safe_eval(expr: str) -> float:
    """Evaluate an expression containing only basic arithmetic syntax.

    Supported operations are ``+``, ``-``, ``*``, ``/``, ``**``, unary
    ``+``/``-``, and parentheses. Power exponents with magnitude greater than
    1000 are rejected.
    """
    if not isinstance(expr, str) or not expr.strip():
        raise ValueError("expression must be a non-empty string")

    try:
        tree = ast.parse(expr.strip(), mode="eval")
        result = _evaluate(tree.body)
    except (SyntaxError, RecursionError) as exc:
        raise ValueError("invalid arithmetic expression") from exc

    if isinstance(result, complex):
        raise ValueError("expression produced a complex result")
    return float(result)


def _evaluate(node: ast.AST) -> float:
    if isinstance(node, ast.Constant):
        value = node.value
        if type(value) not in (int, float):
            raise ValueError("only real numeric literals are allowed")
        return float(value)

    if isinstance(node, ast.UnaryOp):
        operation = _UNARY_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("unsupported unary operator")
        return operation(_evaluate(node.operand))

    if isinstance(node, ast.BinOp):
        if isinstance(node.op, ast.Pow):
            try:
                exponent = _evaluate(node.right)
            except OverflowError as exc:
                raise ValueError("power exponent is too large") from exc

            if abs(exponent) > 1000:
                raise ValueError("power exponent magnitude exceeds 1000")

            base = _evaluate(node.left)
            result = operator.pow(base, exponent)
            if isinstance(result, complex):
                raise ValueError("complex results are not supported")
            return result

        operation = _BINARY_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("unsupported binary operator")
        return operation(_evaluate(node.left), _evaluate(node.right))

    raise ValueError(f"unsupported syntax: {type(node).__name__}")
