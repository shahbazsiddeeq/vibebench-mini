import ast


def find_bare_excepts(source: str) -> list[int]:
    """Return line numbers of all bare ``except:`` clauses in Python source."""
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError("source is not valid Python") from exc

    return sorted(
        node.lineno
        for node in ast.walk(tree)
        if isinstance(node, ast.ExceptHandler) and node.type is None
    )
