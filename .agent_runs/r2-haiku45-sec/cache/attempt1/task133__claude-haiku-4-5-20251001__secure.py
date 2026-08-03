import ast
from typing import Union


def docstring_coverage(source: str) -> float:
    """
    Parse source code and return the fraction of functions and classes with docstrings.
    
    Args:
        source: Python source code as a string
        
    Returns:
        Fraction of documented functions/classes (0.0 to 1.0).
        Returns 1.0 if there are no function or class definitions.
        
    Raises:
        ValueError: If source contains syntax errors
    """
    if not isinstance(source, str):
        raise ValueError("source must be a string")
    
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Syntax error in source: {e}")
    
    documented_count = 0
    total_count = 0
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            total_count += 1
            if ast.get_docstring(node) is not None:
                documented_count += 1
    
    if total_count == 0:
        return 1.0
    
    return documented_count / total_count
