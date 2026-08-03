import ast
import re

def non_snake_case_functions(source):
    """
    Parses source with ast and returns, in source order (by line then column),
    the names of every function definition whose name does not match
    ^[a-z_][a-z0-9_]*$. This includes top-level functions, nested functions,
    async functions, and methods defined inside a class body; class names
    themselves are never checked, and dunder methods such as __init__ are
    snake_case so they are not reported. Raises ValueError on syntax errors.

    Args:
        source (str): The Python source code to parse.

    Returns:
        list: A list of function names that are not in snake_case,
              ordered by their appearance in the source code.

    Raises:
        ValueError: If the source code contains syntax errors.
    """
    non_snake_case_names = []
    snake_case_pattern = re.compile(r"^[a-z_][a-z0-9_]*$")

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Syntax error in source code: {e}") from e

    # Collect all function definitions with their line and column numbers
    function_nodes = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            function_nodes.append(node)

    # Sort functions by their appearance in the source code
    function_nodes.sort(key=lambda n: (n.lineno, n.col_offset))

    for node in function_nodes:
        if not snake_case_pattern.match(node.name):
            non_snake_case_names.append(node.name)

    return non_snake_case_names
