import ast


def find_bare_excepts(source: str) -> list[int]:
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}")

    result = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            result.append(node.lineno)

    return sorted(result)
