import ast


def docstring_coverage(source):
    """
    Calculate the fraction of functions and classes that have docstrings.
    
    Args:
        source: Python source code as a string
        
    Returns:
        Float between 0.0 and 1.0 representing the fraction of documented
        functions and classes. Returns 1.0 if there are no definitions.
        
    Raises:
        ValueError: If the source code has syntax errors
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Syntax error in source: {e}")
    
    total_definitions = 0
    documented_definitions = 0
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            total_definitions += 1
            if has_docstring(node):
                documented_definitions += 1
    
    if total_definitions == 0:
        return 1.0
    
    return documented_definitions / total_definitions


def has_docstring(node):
    """
    Check if a function or class definition has a docstring.
    
    Args:
        node: An AST node (FunctionDef, AsyncFunctionDef, or ClassDef)
        
    Returns:
        True if the node has a docstring, False otherwise
    """
    if not node.body:
        return False
    
    first_stmt = node.body[0]
    
    # Check if the first statement is an Expr node containing a string
    if isinstance(first_stmt, ast.Expr):
        # In Python 3.8+, string constants are ast.Constant with string value
        # In earlier versions, they might be ast.Str
        if isinstance(first_stmt.value, ast.Constant):
            return isinstance(first_stmt.value.value, str)
        elif isinstance(first_stmt.value, ast.Str):
            return True
    
    return False
