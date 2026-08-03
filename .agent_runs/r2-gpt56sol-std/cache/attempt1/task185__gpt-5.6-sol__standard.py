import ast


def find_mutable_defaults(source: str) -> list[tuple[str, int]]:
    """Return functions whose parameters have mutable literal defaults."""
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError("source is not valid Python") from exc

    mutable_types = (ast.List, ast.Dict, ast.Set)
    results: list[tuple[str, int]] = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            defaults = (*node.args.defaults, *node.args.kw_defaults)
            if any(isinstance(default, mutable_types) for default in defaults):
                results.append((node.name, node.lineno))

    return sorted(results, key=lambda item: (item[1], item[0]))
