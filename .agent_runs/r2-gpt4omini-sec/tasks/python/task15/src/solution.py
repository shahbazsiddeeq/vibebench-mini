import ast
import operator

class SafeEvalVisitor(ast.NodeVisitor):
    def __init__(self):
        self.result = None

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = self.get_operator(node.op)
        return op(left, right)

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op = self.get_operator(node.op)
        return op(operand)

    def visit_Constant(self, node):
        return float(node.value)

    def visit_Expression(self, node):
        return self.visit(node.body)

    def get_operator(self, op):
        if isinstance(op, ast.Add):
            return operator.add
        elif isinstance(op, ast.Sub):
            return operator.sub
        elif isinstance(op, ast.Mult):
            return operator.mul
        elif isinstance(op, ast.Div):
            return operator.truediv
        elif isinstance(op, ast.Pow):
            return self.safe_pow
        else:
            raise ValueError("Invalid expression")

    def safe_pow(self, base, exp):
        if abs(exp) > 1000:
            raise ValueError("Exponent too large")
        return operator.pow(base, exp)

def safe_eval(expr: str) -> float:
    # Validate input
    if not isinstance(expr, str):
        raise ValueError("Input must be a string")
    
    # Parse the expression
    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError:
        raise ValueError("Invalid expression")

    # Create a visitor and visit the parsed tree
    visitor = SafeEvalVisitor()
    return visitor.visit(tree)
