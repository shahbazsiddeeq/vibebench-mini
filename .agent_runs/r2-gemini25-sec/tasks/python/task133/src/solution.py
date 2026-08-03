import ast

def docstring_coverage(source: str) -> float:
    """
    Parses source with ast and returns the fraction of all function (FunctionDef/AsyncFunctionDef)
    and class (ClassDef) definitions that have a docstring.
    Returns 1.0 if there are no function or class definitions.
    Raises ValueError on syntax errors.

    Args:
        source: The Python source code as a string.

    Returns:
        The fraction of documented function and class definitions as a float.

    Raises:
        ValueError: If the source code contains a syntax error.
    """
    if not isinstance(source, str):
        raise TypeError("Input 'source' must be a string.")

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Syntax error in source code: {e}") from e

    total_definitions = 0
    documented_definitions = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            total_definitions += 1
            # Check if the node has a docstring
            # ast.get_docstring returns None if no docstring is found
            if ast.get_docstring(node) is not None:
                documented_definitions += 1

    if total_definitions == 0:
        return 1.0
    else:
        return documented_definitions / total_definitions
