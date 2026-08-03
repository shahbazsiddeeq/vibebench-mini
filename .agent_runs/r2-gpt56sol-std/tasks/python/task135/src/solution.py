import ast


def unused_imports(source: str) -> list[str]:
    """Return imported names that are never used as an ``ast.Name``."""
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError(str(exc)) from exc

    used_names = {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name)
    }

    imports: list[tuple[int, int, int, str]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for index, alias in enumerate(node.names):
                bound_name = alias.asname or alias.name.split(".", 1)[0]
                imports.append(
                    (node.lineno, node.col_offset, index, bound_name)
                )
        elif isinstance(node, ast.ImportFrom):
            for index, alias in enumerate(node.names):
                if alias.name == "*":
                    continue
                bound_name = alias.asname or alias.name
                imports.append(
                    (node.lineno, node.col_offset, index, bound_name)
                )

    imports.sort(key=lambda item: item[:3])
    return [
        bound_name
        for _, _, _, bound_name in imports
        if bound_name not in used_names
    ]
