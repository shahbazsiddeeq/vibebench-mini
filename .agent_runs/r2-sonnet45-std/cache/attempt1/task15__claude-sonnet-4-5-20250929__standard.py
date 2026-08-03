import ast

def safe_eval(expr: str) -> float:
    """
    Safely evaluates an arithmetic expression containing only numeric literals,
    binary operators (+, -, *, /, **), unary +/-, and parentheses.
    
    Args:
        expr: The arithmetic expression to evaluate
        
    Returns:
        The result as a float
        
    Raises:
        ValueError: If the expression contains disallowed syntax or exponent > 1000
        ZeroDivisionError: If division by zero occurs
    """
    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError:
        raise ValueError("Invalid syntax")
    
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        
        elif isinstance(node, ast.Constant):
            # In Python 3.8+, numbers are ast.Constant
            if isinstance(node.value, (int, float)):
                return float(node.value)
            else:
                raise ValueError("Only numeric constants allowed")
        
        elif isinstance(node, ast.Num):
            # For older Python versions (ast.Num is deprecated but may still appear)
            return float(node.n)
        
        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            if isinstance(node.op, ast.UAdd):
                return operand
            elif isinstance(node.op, ast.USub):
                return -operand
            else:
                raise ValueError("Only unary + and - allowed")
        
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            
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
                # Check exponent magnitude before computing
                if abs(right) > 1000:
                    raise ValueError("Exponent magnitude exceeds 1000")
                return left ** right
            else:
                raise ValueError("Only +, -, *, /, ** operators allowed")
        
        else:
            raise ValueError("Disallowed syntax in expression")
    
    result = _eval(tree)
    return float(result)
