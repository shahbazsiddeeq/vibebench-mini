# src/solution.py

import ast

def unused_imports(source: str) -> list[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError("Syntax error in source code") from e

    # Collect all imports and their aliases
    imports = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports[alias.name] = alias.asname or alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:  # Only consider top-level imports
                for alias in node.names:
                    imports[alias.name] = alias.asname or alias.name

    # Collect all used names
    used_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used_names.add(node.id)

    # Determine unused imports
    unused = []
    for name, alias in imports.items():
        if name not in used_names:
            unused.append(alias)

    return unused
