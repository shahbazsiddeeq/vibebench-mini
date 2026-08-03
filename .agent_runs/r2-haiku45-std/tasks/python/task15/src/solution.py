import ast
import operator

def safe_eval(expr: str) -> float:
    """
    Safely evaluates an arithmetic expression containing only:
    - numeric literals
    - binary operators: + - * / **
    - unary operators: + -
    - parentheses
    
    Returns the result as a float.
    Raises ValueError for any disallowed syntax or exponent magnitude > 1000.
    Raises ZeroDivisionError for division by zero.
    """
    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")
    
    return _eval_node(tree.body)


def _eval_node(node):
    """Recursively evaluate an AST node."""
    
    # Numeric literals
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return float(node.value)
        else:
            raise ValueError(f"Unsupported constant type: {type(node.value)}")
    
    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        elif isinstance(node.op, ast.USub):
            return -operand
        else:
            raise ValueError(f"Unsupported unary operator: {type(node.op)}")
    
    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        
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
            # Check exponent magnitude to prevent resource exhaustion
            if abs(right) > 1000:
                raise ValueError(f"Exponent magnitude {abs(right)} exceeds maximum of 1000")
            return left ** right
        else:
            raise ValueError(f"Unsupported binary operator: {type(node.op)}")
    
    # Reject everything else
    raise ValueError(f"Unsupported node type: {type(node).__name__}")
