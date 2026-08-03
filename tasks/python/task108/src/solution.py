import ast

# Decision-point nodes that count as a branch. Note: ast.If covers both `if`
# and `elif` (elif parses as a nested If); a bare `else` and the `try` header
# itself have no dedicated node here and are not counted.
_BRANCH_NODES = (ast.If, ast.For, ast.While, ast.ExceptHandler)


def estimate_complexity(func_source: str) -> dict:
    if not isinstance(func_source, str) or not func_source.strip():
        raise ValueError("source must be a non-empty string")
    try:
        tree = ast.parse(func_source)
    except SyntaxError as e:
        raise ValueError(f"unparseable source: {e}")

    body = tree.body
    if len(body) != 1 or not isinstance(
        body[0], (ast.FunctionDef, ast.AsyncFunctionDef)
    ):
        raise ValueError("source must define exactly one top-level function")

    lines = len([ln for ln in func_source.splitlines() if ln.strip()])
    branches = 0
    returns = 0

    for node in ast.walk(tree):
        if isinstance(node, _BRANCH_NODES):
            branches += 1
        elif isinstance(node, ast.Return):
            returns += 1

    return {"lines": lines, "branches": branches, "returns": returns}
