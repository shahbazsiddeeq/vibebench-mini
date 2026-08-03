import ast
import operator
from typing import Union


def safe_eval(expr: str) -> float:
    """
    Safely evaluates an arithmetic expression containing only:
    - Numeric literals
    - Binary operators: +, -, *, /, **
    - Unary operators: +, -
    - Parentheses
    
    Returns the result as a float.
    
    Raises:
        ValueError: If the expression contains disallowed syntax or exponent magnitude > 1000
        ZeroDivisionError: If division by zero occurs
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")
    
    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}")
    
    return _eval_node(tree.body)


def _eval_node(node: ast.expr) -> float:
    """
    Recursively evaluates an AST node, allowing only safe arithmetic operations.
    """
    if isinstance(node, ast.Constant):
        # Handle numeric constants
        if isinstance(node.value, (int, float)):
            return float(node.value)
        else:
            raise ValueError(f"Unsupported constant type: {type(node.value)}")
    
    elif isinstance(node, ast.Num):
        # For older Python versions that use ast.Num
        return float(node.n)
    
    elif isinstance(node, ast.UnaryOp):
        # Handle unary + and -
        operand = _eval_node(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        elif isinstance(node.op, ast.USub):
            return -operand
        else:
            raise ValueError(f"Unsupported unary operator: {type(node.op)}")
    
    elif isinstance(node, ast.BinOp):
        # Handle binary operations
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
                raise ValueError("Exponent magnitude exceeds 1000")
            return left ** right
        else:
            raise ValueError(f"Unsupported binary operator: {type(node.op)}")
    
    else:
        # Reject all other node types (names, calls, subscripts, lambdas, etc.)
        raise ValueError(f"Unsupported expression type: {type(node).__name__}")
