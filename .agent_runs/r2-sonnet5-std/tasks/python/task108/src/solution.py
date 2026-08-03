import ast


def estimate_complexity(func_source: str) -> dict:
    if not func_source or not func_source.strip():
        raise ValueError("Empty source")

    try:
        tree = ast.parse(func_source)
    except SyntaxError:
        raise ValueError("Could not parse source")

    top_level_funcs = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]

    if len(top_level_funcs) != 1:
        raise ValueError("Source must define exactly one top-level function")

    func_node = top_level_funcs[0]

    lines = [line for line in func_source.splitlines() if line.strip() != ""]
    line_count = len(lines)

    branches = 0
    returns = 0

    for node in ast.walk(func_node):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
            branches += 1
        elif isinstance(node, ast.Return):
            returns += 1

    return {"lines": line_count, "branches": branches, "returns": returns}
