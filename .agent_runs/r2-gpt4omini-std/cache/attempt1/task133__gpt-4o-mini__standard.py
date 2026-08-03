# src/solution.py

import ast

def docstring_coverage(source: str) -> float:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Syntax error in the provided source code.")

    total_definitions = 0
    documented_definitions = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            total_definitions += 1
            if ast.get_docstring(node):
                documented_definitions += 1

    if total_definitions == 0:
        return 1.0

    return documented_definitions / total_definitions
