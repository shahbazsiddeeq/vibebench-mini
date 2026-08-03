import ast
import re

def non_snake_case_functions(source: str) -> list[str]:
    """
    Parses Python source code and returns a list of function names that do not
    adhere to snake_case naming conventions.

    A function name is considered non-snake_case if it does not match the regex
    ^[a-z_][a-z0-9_]*$. This includes top-level functions, nested functions,
    async functions, and methods defined inside a class body. Class names
    themselves are never checked. Dunder methods (e.g., __init__) are
    considered snake_case and are not reported.

    Args:
        source: A string containing Python source code.

    Returns:
        A list of strings, where each string is the name of a function that
        does not follow snake_case, ordered by their appearance in the source
        code (line then column).

    Raises:
        ValueError: If the provided source code has a syntax error.
        TypeError: If the input 'source' is not a string.
    """
    if not isinstance(source, str):
        raise TypeError("Input 'source' must be a string.")

    # Regex for valid snake_case names
    # ^[a-z_]  - Starts with a lowercase letter or an underscore
    # [a-z0-9_]* - Followed by zero or more lowercase letters, digits, or underscores
    SNAKE_CASE_REGEX = re.compile(r"^[a-z_][a-z0-9_]*$")

    non_snake_case_names = []

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        # Re-raise as ValueError to match the specified behavior
        raise ValueError(f"Syntax error in source code: {e}") from e

    # Use a list of tuples (line, col, name) to maintain source order
    # before extracting just the names.
    found_names_with_pos = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Check if the function name matches the snake_case pattern
            if not SNAKE_CASE_REGEX.fullmatch(node.name):
                found_names_with_pos.append((node.lineno, node.col_offset, node.name))

    # Sort by line number, then by column offset to ensure source order
    found_names_with_pos.sort()

    # Extract just the names
    for _, _, name in found_names_with_pos:
        non_snake_case_names.append(name)

    return non_snake_case_names
