import ast

def estimate_complexity(func_source: str) -> dict:
    if not func_source.strip():
        raise ValueError("Source is empty")

    try:
        tree = ast.parse(func_source)
    except SyntaxError:
        raise ValueError("Source cannot be parsed")

    # Ensure there is exactly one top-level function
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    if len(functions) != 1:
        raise ValueError("Source does not define exactly one top-level function")

    # Initialize counts
    lines = 0
    branches = 0
    returns = 0

    # Count non-blank lines
    lines = sum(1 for line in func_source.splitlines() if line.strip())

    # Traverse the AST to count branches and returns
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
            branches += 1
        elif isinstance(node, ast.Return):
            returns += 1

    return {"lines": lines, "branches": branches, "returns": returns}
