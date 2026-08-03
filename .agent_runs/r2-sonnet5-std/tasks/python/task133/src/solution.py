import ast


def docstring_coverage(source):
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    total = 0
    documented = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            total += 1
            if ast.get_docstring(node) is not None:
                documented += 1

    if total == 0:
        return 1.0

    return documented / total
