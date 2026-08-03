import ast

def docstring_coverage(source):
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid syntax")

    total_defs = 0
    documented_defs = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            total_defs += 1
            if ast.get_docstring(node) is not None:
                documented_defs += 1

    if total_defs == 0:
        return 1.0

    return documented_defs / total_defs
