import ast


def docstring_coverage(source: str) -> float:
    """Return the fraction of function and class definitions with docstrings.

    Both synchronous and asynchronous functions are included, as are nested
    definitions. If no definitions exist, 1.0 is returned. Invalid Python
    syntax raises ValueError.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError("invalid Python syntax") from exc

    definitions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    ]

    if not definitions:
        return 1.0

    documented = sum(ast.get_docstring(node, clean=False) is not None for node in definitions)
    return documented / len(definitions)
