import ast
import operator

class SafeEval(ast.NodeVisitor):
    def visit_Module(self, node):
        if len(node.body) != 1 or not isinstance(node.body[0], ast.Expr):
            raise ValueError("Expression must contain a single expression.")
        return self.visit(node.body[0])

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise ValueError(f"Unsupported constant type: {type(node.value)}")

    def visit_Num(self, node):  # For Python < 3.8
        return float(node.n)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if isinstance(node.op, ast.Add):
            return operator.add(left, right)
        elif isinstance(node.op, ast.Sub):
            return operator.sub(left, right)
        elif isinstance(node.op, ast.Mult):
            return operator.mul(left, right)
        elif isinstance(node.op, ast.Div):
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return operator.truediv(left, right)
        elif isinstance(node.op, ast.Pow):
            if abs(right) > 1000:
                raise ValueError("Exponent magnitude too large")
            return operator.pow(left, right)
        else:
            raise ValueError(f"Unsupported binary operator: {type(node.op)}")

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        if isinstance(node.op, ast.UAdd):
            return operand
        elif isinstance(node.op, ast.USub):
            return -operand
        else:
            raise ValueError(f"Unsupported unary operator: {type(node.op)}")

    def visit_Name(self, node):
        raise ValueError(f"Names are not allowed: {node.id}")

    def visit_Call(self, node):
        raise ValueError("Function calls are not allowed")

    def visit_Attribute(self, node):
        raise ValueError("Attribute access is not allowed")

    def visit_Subscript(self, node):
        raise ValueError("Subscripts are not allowed")

    def visit_ListComp(self, node):
        raise ValueError("List comprehensions are not allowed")

    def visit_SetComp(self, node):
        raise ValueError("Set comprehensions are not allowed")

    def visit_GeneratorExp(self, node):
        raise ValueError("Generator expressions are not allowed")

    def visit_DictComp(self, node):
        raise ValueError("Dictionary comprehensions are not allowed")

    def visit_Lambda(self, node):
        raise ValueError("Lambda expressions are not allowed")

    def generic_visit(self, node):
        # Catch any other AST nodes that are not explicitly allowed
        raise ValueError(f"Unsupported syntax: {type(node).__name__}")

def safe_eval(expr: str) -> float:
    """
    Safely evaluates an arithmetic expression.

    Args:
        expr: The string expression to evaluate.

    Returns:
        The result of the evaluation as a float.

    Raises:
        ValueError: If the expression contains unsupported syntax,
                    or if a power operation's exponent magnitude is too large.
        ZeroDivisionError: If division by zero occurs.
    """
    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from e

    evaluator = SafeEval()
    return evaluator.visit(tree)
