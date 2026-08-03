# src/solution.py

import ast

class SafeEvalVisitor(ast.NodeVisitor):
    def visit(self, node):
        if isinstance(node, ast.Expression):
            return self.visit(node.body)
        elif isinstance(node, (ast.Num, ast.UnaryOp, ast.BinOp, ast.BinOp, ast.Compare)):
            return self.generic_visit(node)
        elif isinstance(node, ast.Call):
            raise ValueError("Invalid expression: function calls are not allowed.")
        elif isinstance(node, ast.Name):
            raise ValueError("Invalid expression: names are not allowed.")
        elif isinstance(node, ast.Attribute):
            raise ValueError("Invalid expression: attribute access is not allowed.")
        elif isinstance(node, ast.Subscript):
            raise ValueError("Invalid expression: subscripts are not allowed.")
        elif isinstance(node, ast.Lambda):
            raise ValueError("Invalid expression: lambdas are not allowed.")
        elif isinstance(node, ast.Pow):
            if isinstance(node.right, ast.Num) and abs(node.right.n) > 1000:
                raise ValueError("Exponent too large.")
            return self.generic_visit(node)
        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            return self.generic_visit(node)
        else:
            raise ValueError("Invalid expression: unsupported operation.")

    def visit_Num(self, node):
        return node.n

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        elif isinstance(node.op, ast.USub):
            return -operand
        raise ValueError("Invalid expression: unsupported unary operation.")

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            if right == 0:
                raise ZeroDivisionError("Division by zero.")
            return left / right
        elif isinstance(node.op, ast.Pow):
            if abs(right) > 1000:
                raise ValueError("Exponent too large.")
            return left ** right
        raise ValueError("Invalid expression: unsupported binary operation.")

def safe_eval(expr: str) -> float:
    try:
        tree = ast.parse(expr, mode='eval')
        visitor = SafeEvalVisitor()
        result = visitor.visit(tree)
        return float(result)
    except ZeroDivisionError:
        raise
    except Exception:
        raise ValueError("Invalid expression.")
