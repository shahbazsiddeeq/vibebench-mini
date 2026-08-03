import ast


def docstring_coverage(source: str) -> float:
    """
    Calculate the fraction of functions and classes that have docstrings.
    
    Args:
        source: Python source code as a string
        
    Returns:
        Float between 0.0 and 1.0 representing the fraction of documented
        definitions. Returns 1.0 if there are no definitions.
        
    Raises:
        ValueError: If the source code has syntax errors
    """
    # Validate input
    if not isinstance(source, str):
        raise ValueError("Source must be a string")
    
    # Parse the source code
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Syntax error in source code: {e}")
    
    # Count total definitions and documented definitions
    total_definitions = 0
    documented_definitions = 0
    
    # Walk through all nodes in the AST
    for node in ast.walk(tree):
        # Check if node is a function or class definition
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            total_definitions += 1
            
            # Check if it has a docstring
            # A docstring is the first statement in the body and must be a string
            if (node.body and 
                isinstance(node.body[0], ast.Expr) and 
                isinstance(node.body[0].value, ast.Constant) and 
                isinstance(node.body[0].value.value, str)):
                documented_definitions += 1
    
    # Return 1.0 if there are no definitions
    if total_definitions == 0:
        return 1.0
    
    # Calculate and return the coverage
    return documented_definitions / total_definitions
