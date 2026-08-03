import ast


def estimate_complexity(func_source: str) -> dict:
    """Estimate line, branch, and return counts for one top-level function."""
    if not isinstance(func_source, str) or not func_source.strip():
        raise ValueError("source must be a non-empty string")

    try:
        tree = ast.parse(func_source)
    except (SyntaxError, ValueError, TypeError) as exc:
        raise ValueError("source cannot be parsed") from exc

    function_types = (ast.FunctionDef, ast.AsyncFunctionDef)
    functions = [
        node for node in tree.body
        if isinstance(node, function_types)
    ]

    if len(functions) != 1:
        raise ValueError("source must define exactly one top-level function")

    function = functions[0]
    branch_types = (ast.If, ast.For, ast.While, ast.ExceptHandler)

    branches = 0
    returns = 0

    for node in ast.walk(function):
        if isinstance(node, branch_types):
            branches += 1
        if isinstance(node, ast.Return):
            returns += 1

    lines = sum(1 for line in func_source.splitlines() if line.strip())

    return {
        "lines": lines,
        "branches": branches,
        "returns": returns,
    }
