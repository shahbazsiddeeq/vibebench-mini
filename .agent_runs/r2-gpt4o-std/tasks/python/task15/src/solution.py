import ast
import operator

class SafeEvalVisitor(ast.NodeVisitor):
    def __init__(self):
        self.allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: self.safe_pow,
            ast.UAdd: operator.pos,
            ast.USub: operator.neg,
        }

    def safe_pow(self, base, exp):
        if abs(exp) > 1000:
            raise ValueError("Exponent magnitude too large")
        return operator.pow(base, exp)

    def visit(self, node):
        if isinstance(node, ast.Expression):
            return self.visit(node.body)
        elif isinstance(node, ast.BinOp):
            left = self.visit(node.left)
            right = self.visit(node.right)
            op_type = type(node.op)
            if op_type in self.allowed_operators:
                return self.allowed_operators[op_type](left, right)
            else:
                raise ValueError("Unsupported operation")
        elif isinstance(node, ast.UnaryOp):
            operand = self.visit(node.operand)
            op_type = type(node.op)
            if op_type in self.allowed_operators:
                return self.allowed_operators[op_type](operand)
            else:
                raise ValueError("Unsupported operation")
        elif isinstance(node, ast.Num):
            return float(node.n)
        elif isinstance(node, ast.Paren):
            return self.visit(node.value)
        else:
            raise ValueError("Unsupported syntax")

def safe_eval(expr: str) -> float:
    try:
        tree = ast.parse(expr, mode='eval')
        visitor = SafeEvalVisitor()
        return visitor.visit(tree)
    except ZeroDivisionError:
        raise
    except Exception:
        raise ValueError("Invalid expression")
