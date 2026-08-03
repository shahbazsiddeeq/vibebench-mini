"""
src/solution.py

Safe arithmetic expression evaluator.

Provides `safe_eval(expr: str) -> float` which evaluates simple arithmetic
expressions consisting of numeric literals, the binary operators
+ - * / **, unary + and -, and parentheses. Any other syntax (names,
attribute access, function calls, subscripts, comprehensions, lambdas,
etc.) raises ValueError. Division by zero raises ZeroDivisionError.
To avoid resource exhaustion, exponentiation with an exponent whose
magnitude exceeds 1000 raises ValueError.
"""

import ast

__all__ = ["safe_eval"]

_MAX_EXPONENT_MAGNITUDE = 1000

# Allowed binary operators and their implementations.
_ALLOWED_BINOPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.Pow: lambda a, b: a ** b,
}

# Allowed unary operators and their implementations.
_ALLOWED_UNARYOPS = {
    ast.UAdd: lambda a: +a,
    ast.USub: lambda a: -a,
}


def safe_eval(expr: str) -> float:
    """
    Safely evaluate an arithmetic expression and return the result as a float.

    Only numeric literals, +, -, *, /, **, unary +/-, and parentheses are
    permitted. Any other construct raises ValueError. Division by zero
    raises ZeroDivisionError. Exponents with magnitude greater than 1000
    raise ValueError to avoid resource exhaustion.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string.")

    try:
        tree = ast.parse(expr, mode="eval")
    except (SyntaxError, ValueError):
        raise ValueError("Invalid expression syntax.")

    result = _eval_node(tree.body)

    try:
        return float(result)
    except (TypeError, OverflowError):
        raise ValueError("Expression did not evaluate to a numeric value.")


def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Constant):
        # Only allow int/float literals, not strings/bytes/None/etc.
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise ValueError("Only numeric literals are allowed.")
        return node.value

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_BINOPS:
            raise ValueError(f"Operator {op_type.__name__} is not allowed.")

        left = _eval_node(node.left)
        right = _eval_node(node.right)

        if op_type is ast.Pow:
            if abs(right) > _MAX_EXPONENT_MAGNITUDE:
                raise ValueError(
                    "Exponent magnitude too large; refusing to compute."
                )

        if op_type is ast.Div and right == 0:
            raise ZeroDivisionError("Division by zero.")

        try:
            return _ALLOWED_BINOPS[op_type](left, right)
        except ZeroDivisionError:
            raise
        except OverflowError:
            raise ValueError("Result too large to compute.")

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARYOPS:
            raise ValueError(f"Unary operator {op_type.__name__} is not allowed.")
        operand = _eval_node(node.operand)
        return _ALLOWED_UNARYOPS[op_type](operand)

    # Anything else (Name, Call, Attribute, Subscript, Lambda,
    # comprehensions, function defs, etc.) is disallowed.
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")
