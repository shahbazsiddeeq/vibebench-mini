import ast


def find_bare_excepts(source: str) -> list[int]:
    """
    Parses a string of Python source and returns the sorted-ascending list of
    1-based line numbers of every bare except clause (i.e., `except:`).

    Args:
        source: The Python source code as a string.

    Returns:
        A list of 1-based line numbers of bare except clauses.

    Raises:
        ValueError: If the source is not valid Python.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError("Invalid Python source code") from e

    bare_except_lines = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                bare_except_lines.append(node.lineno)

    return sorted(bare_except_lines)
