import ast


def docstring_coverage(source):
    """
    Calculate the fraction of functions and classes that have docstrings.
    
    Args:
        source: Python source code as a string
        
    Returns:
        float: Fraction of documented functions/classes (1.0 if none exist)
        
    Raises:
        ValueError: If source has syntax errors
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Syntax error in source: {e}")
    
    # Count all function and class definitions
    total_definitions = 0
    documented_definitions = 0
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            total_definitions += 1
            
            # Check if the node has a docstring
            docstring = ast.get_docstring(node)
            if docstring is not None:
                documented_definitions += 1
    
    # If no definitions, return 1.0
    if total_definitions == 0:
        return 1.0
    
    return documented_definitions / total_definitions
