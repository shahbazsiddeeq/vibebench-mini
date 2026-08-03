import ast
import operator

_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def safe_eval(expr: str) -> float:
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Invalid expression: {e}")

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, bool):
                raise ValueError("Booleans are not allowed")
            if isinstance(node.value, (int, float)):
                return float(node.value)
            raise ValueError("Only numeric constants are allowed")
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in _BIN_OPS:
                raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
            left = _eval(node.left)
            right = _eval(node.right)
            if op_type is ast.Pow:
                if abs(right) > 1000:
                    raise ValueError("Exponent magnitude too large")
                return operator.pow(left, right)
            if op_type is ast.Div:
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                return operator.truediv(left, right)
            return _BIN_OPS[op_type](left, right)
        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in _UNARY_OPS:
                raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
            operand = _eval(node.operand)
            return _UNARY_OPS[op_type](operand)
        else:
            raise ValueError(f"Unsupported syntax: {type(node).__name__}")

    return _eval(tree)
