import ast

def find_bare_excepts(source: str) -> list[int]:
    """
    Parses a string of Python source and returns the sorted-ascending list of
    1-based line numbers of every bare except clause (ast.ExceptHandler whose
    type attribute is None, i.e., `except:`).

    Args:
        source: The Python source code as a string.

    Returns:
        A list of 1-based line numbers where bare except clauses are found.

    Raises:
        ValueError: If the source is not valid Python code.
    """
    if not isinstance(source, str):
        raise ValueError("Input 'source' must be a string.")

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source code: {e}") from e

    bare_except_lines = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                bare_except_lines.append(node.lineno)

    bare_except_lines.sort()
    return bare_except_lines
