import ast

def find_mutable_defaults(source: str) -> list[tuple[str, int]]:
    """
    Parses a string of Python source and returns a list of (function_name, lineno)
    for functions that have at least one parameter with a mutable default value.

    A default counts as mutable if its AST node is a list display ([...]/[]),
    a dict display ({...}/{}), or a set display ({1, 2}).
    Tuple defaults, string/number/None/bool constants, and calls like list()
    or dict() do NOT count.

    Args:
        source: The Python source code as a string.

    Returns:
        A list of tuples, where each tuple contains the function name and the
        1-based line number of the 'def' or 'async def' statement.
        The result is sorted ascending by (lineno, function_name).

    Raises:
        ValueError: If the source is not valid Python.
    """
    if not isinstance(source, str):
        raise ValueError("Input 'source' must be a string.")

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}") from e

    mutable_defaults_found = {} # Use a dict to store unique (name, lineno) and handle sorting later

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            function_name = node.name
            lineno = node.lineno

            # Check ordinary arguments
            for default_expr in node.args.defaults:
                if isinstance(default_expr, (ast.List, ast.Dict, ast.Set)):
                    mutable_defaults_found[(function_name, lineno)] = None
                    break # Found one mutable default, no need to check others for this function

            if (function_name, lineno) in mutable_defaults_found:
                continue # Already found a mutable default for this function

            # Check keyword-only arguments
            for default_expr in node.args.kw_defaults:
                if default_expr is not None and isinstance(default_expr, (ast.List, ast.Dict, ast.Set)):
                    mutable_defaults_found[(function_name, lineno)] = None
                    break # Found one mutable default, no need to check others for this function

    result = sorted(list(mutable_defaults_found.keys()), key=lambda x: (x[1], x[0]))
    return result
