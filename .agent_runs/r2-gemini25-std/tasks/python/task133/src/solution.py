import ast

def docstring_coverage(source: str) -> float:
    """
    Calculates the fraction of function and class definitions that have a docstring.

    Args:
        source: The Python source code as a string.

    Returns:
        The fraction of documented function/class definitions. Returns 1.0 if
        there are no definitions.

    Raises:
        ValueError: If the source code has a syntax error.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError("Syntax error in source code") from e

    total_definitions = 0
    documented_definitions = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            total_definitions += 1
            if ast.get_docstring(node) is not None:
                documented_definitions += 1

    if total_definitions == 0:
        return 1.0
    else:
        return documented_definitions / total_definitions
