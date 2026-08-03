# src/solution.py

import ast

def docstring_coverage(source: str) -> float:
    """
    Calculate the fraction of function and class definitions that have a docstring.

    Args:
        source (str): The source code to analyze.

    Returns:
        float: The fraction of documented definitions, or 1.0 if there are none.

    Raises:
        ValueError: If there is a syntax error in the source code.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid syntax in the provided source code.")

    total_definitions = 0
    documented_definitions = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            total_definitions += 1
            if ast.get_docstring(node):
                documented_definitions += 1

    if total_definitions == 0:
        return 1.0

    return documented_definitions / total_definitions
