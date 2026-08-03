import ast

class SafeEval(ast.NodeVisitor):
    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        elif isinstance(node.op, ast.USub):
            return -operand
        raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")

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
                raise ZeroDivisionError("division by zero")
            return left / right
        elif isinstance(node.op, ast.Pow):
            if abs(right) > 1000:
                raise ValueError("Exponent magnitude too large")
            return left ** right
        raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")

    def visit_Name(self, node):
        raise ValueError(f"Unsupported syntax: Name '{node.id}'")

    def visit_Call(self, node):
        raise ValueError("Unsupported syntax: Function call")

    def visit_Attribute(self, node):
        raise ValueError("Unsupported syntax: Attribute access")

    def visit_Subscript(self, node):
        raise ValueError("Unsupported syntax: Subscript")

    def visit_ListComp(self, node):
        raise ValueError("Unsupported syntax: List comprehension")

    def visit_SetComp(self, node):
        raise ValueError("Unsupported syntax: Set comprehension")

    def visit_DictComp(self, node):
        raise ValueError("Unsupported syntax: Dict comprehension")

    def visit_GeneratorExp(self, node):
        raise ValueError("Unsupported syntax: Generator expression")

    def visit_Lambda(self, node):
        raise ValueError("Unsupported syntax: Lambda expression")

    def generic_visit(self, node):
        # Catch any other AST nodes that are not explicitly allowed
        raise ValueError(f"Unsupported syntax: {type(node).__name__}")

def safe_eval(expr: str) -> float:
    """
    Safely evaluates an arithmetic expression.

    Args:
        expr: The arithmetic expression string.

    Returns:
        The result of the evaluation as a float.

    Raises:
        ValueError: If the expression contains unsupported syntax,
                    or a power operation has an exponent with magnitude > 1000.
        ZeroDivisionError: If division by zero occurs.
    """
    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from e

    evaluator = SafeEval()
    return evaluator.visit(tree)
