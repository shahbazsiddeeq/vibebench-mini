import ast
import operator as op

OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: lambda x: x,
}

# Guard against resource exhaustion: reject power operations whose exponent is
# large enough that computing the result would be astronomically expensive.
_MAX_EXPONENT = 1000


def _eval(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if (
        isinstance(node, ast.Constant)
        and isinstance(node.value, (int, float))
        and not isinstance(node.value, bool)
    ):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        left = _eval(node.left)
        right = _eval(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > _MAX_EXPONENT:
            raise ValueError("exponent too large")
        return OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](_eval(node.operand))
    raise ValueError("unsupported expression")


def safe_eval(expr: str) -> float:
    try:
        tree = ast.parse(expr, mode="eval")
        return _eval(tree)
    except ZeroDivisionError:
        raise
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(str(e))
