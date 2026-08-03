import ast
import operator


def safe_eval(expr: str) -> float:
    """
    Safely evaluate an arithmetic expression containing only:
    - Numeric literals
    - Binary operators: + - * / **
    - Unary operators: + -
    - Parentheses
    
    Args:
        expr: String containing the arithmetic expression
        
    Returns:
        float: Result of the evaluation
        
    Raises:
        ValueError: If expression contains disallowed syntax or exponent magnitude > 1000
        ZeroDivisionError: If division by zero occurs
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")
    
    if not expr or not expr.strip():
        raise ValueError("Expression cannot be empty")
    
    try:
        # Parse the expression into an AST
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")
    
    # Validate and evaluate the AST
    result = _eval_node(tree.body)
    return float(result)


def _eval_node(node):
    """
    Recursively evaluate an AST node, allowing only safe arithmetic operations.
    
    Args:
        node: AST node to evaluate
        
    Returns:
        Numeric result of evaluating the node
        
    Raises:
        ValueError: If node contains disallowed operations
        ZeroDivisionError: If division by zero occurs
    """
    # Numeric constant
    if isinstance(node, ast.Constant):
        # In Python 3.8+, ast.Constant is used for all constants
        if isinstance(node.value, (int, float, complex)):
            if isinstance(node.value, complex):
                raise ValueError("Complex numbers are not allowed")
            return node.value
        else:
            raise ValueError(f"Unsupported constant type: {type(node.value)}")
    
    # For older Python versions, also handle ast.Num
    elif isinstance(node, ast.Num):
        if isinstance(node.n, complex):
            raise ValueError("Complex numbers are not allowed")
        return node.n
    
    # Binary operation (e.g., a + b, a * b)
    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        
        # Map AST operators to Python operators
        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right
        elif isinstance(node.op, ast.Pow):
            # Check exponent magnitude to prevent resource exhaustion
            if abs(right) > 1000:
                raise ValueError("Exponent magnitude must not exceed 1000")
            return left ** right
        else:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
    
    # Unary operation (e.g., -a, +a)
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        
        if isinstance(node.op, ast.UAdd):
            return +operand
        elif isinstance(node.op, ast.USub):
            return -operand
        else:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
    
    # Any other node type is not allowed
    else:
        raise ValueError(f"Unsupported expression type: {type(node).__name__}")
