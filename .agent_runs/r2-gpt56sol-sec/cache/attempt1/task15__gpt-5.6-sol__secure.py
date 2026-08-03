"""Safe arithmetic expression evaluation using a restricted AST."""

from __future__ import annotations

import ast
import math
from typing import Final

__all__ = ["safe_eval"]

_MAX_EXPRESSION_LENGTH: Final = 10_000
_MAX_AST_NODES: Final = 2_000
_MAX_AST_DEPTH: Final = 100
_MAX_INTEGER_BITS: Final = 100_000
_MAX_EXPONENT: Final = 1_000


def _check_integer_size(value: int) -> int:
    if value.bit_length() > _MAX_INTEGER_BITS:
        raise ValueError("numeric result is too large")
    return value


def _evaluate(node: ast.AST, depth: int = 0) -> int | float:
    if depth > _MAX_AST_DEPTH:
        raise ValueError("expression is too deeply nested")

    if isinstance(node, ast.Constant):
        value = node.value
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("only real numeric literals are allowed")
        if isinstance(value, int):
            return _check_integer_size(value)
        return value

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand, depth + 1)
        if isinstance(node.op, ast.UAdd):
            return operand
        if isinstance(node.op, ast.USub):
            return -operand
        raise ValueError("unsupported unary operator")

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left, depth + 1)
        right = _evaluate(node.right, depth + 1)

        if isinstance(node.op, ast.Add):
            result = left + right
        elif isinstance(node.op, ast.Sub):
            result = left - right
        elif isinstance(node.op, ast.Mult):
            if isinstance(left, int) and isinstance(right, int):
                if left and right:
                    estimated_bits = left.bit_length() + right.bit_length()
                    if estimated_bits > _MAX_INTEGER_BITS + 1:
                        raise ValueError("numeric result is too large")
            result = left * right
        elif isinstance(node.op, ast.Div):
            result = left / right
        elif isinstance(node.op, ast.Pow):
            if isinstance(right, float) and not math.isfinite(right):
                raise ValueError("power exponent must be finite")
            if abs(right) > _MAX_EXPONENT:
                raise ValueError("power exponent is too large")

            if (
                isinstance(left, int)
                and isinstance(right, int)
                and right >= 0
                and abs(left) > 1
                and left.bit_length() * right > _MAX_INTEGER_BITS
            ):
                raise ValueError("numeric result is too large")

            result = left**right
        else:
            raise ValueError("unsupported binary operator")

        if isinstance(result, complex):
            raise ValueError("complex results are not supported")
        if isinstance(result, int):
            return _check_integer_size(result)
        if isinstance(result, float):
            return result
        raise ValueError("invalid numeric result")

    raise ValueError("unsupported expression syntax")


def safe_eval(expr: str) -> float:
    """Safely evaluate a restricted arithmetic expression and return a float."""
    if not isinstance(expr, str):
        raise ValueError("expression must be a string")

    expression = expr.strip()
    if not expression:
        raise ValueError("expression must not be empty")
    if len(expression) > _MAX_EXPRESSION_LENGTH:
        raise ValueError("expression is too long")

    try:
        tree = ast.parse(expression, mode="eval")
    except (SyntaxError, ValueError, TypeError, MemoryError, RecursionError) as exc:
        raise ValueError("invalid expression") from None

    try:
        if sum(1 for _ in ast.walk(tree)) > _MAX_AST_NODES:
            raise ValueError("expression is too complex")
        result = _evaluate(tree.body)
        return float(result)
    except ZeroDivisionError:
        raise
    except ValueError:
        raise
    except (OverflowError, MemoryError, RecursionError, TypeError):
        raise ValueError("numeric result is out of range") from None
