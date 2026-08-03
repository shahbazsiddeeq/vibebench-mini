import ast

def estimate_complexity(func_source: str) -> dict:
    """
    Parses the source of a single Python function and estimates its complexity.

    Args:
        func_source: A string containing the source code of a single Python function.

    Returns:
        A dictionary with complexity metrics:
        - "lines": Number of non-blank lines.
        - "branches": Number of decision-point AST nodes (If, For, While, ExceptHandler).
        - "returns": Number of return statements.

    Raises:
        ValueError: If the source is empty, cannot be parsed, or does not define
                    exactly one top-level function.
    """
    if not isinstance(func_source, str):
        raise ValueError("Input func_source must be a string.")
    if not func_source.strip():
        raise ValueError("Source code cannot be empty.")

    try:
        tree = ast.parse(func_source)
    except SyntaxError as e:
        raise ValueError(f"Failed to parse source code: {e}") from e

    function_nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef)]

    if len(function_nodes) != 1:
        raise ValueError("Source code must define exactly one top-level function.")

    # Calculate lines
    non_blank_lines = sum(1 for line in func_source.splitlines() if line.strip())

    # Calculate branches and returns
    branches = 0
    returns = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
            branches += 1
        elif isinstance(node, ast.Return):
            returns += 1

    return {"lines": non_blank_lines, "branches": branches, "returns": returns}
