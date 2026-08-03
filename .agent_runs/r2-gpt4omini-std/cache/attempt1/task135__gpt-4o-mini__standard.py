import ast

def unused_imports(source):
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Syntax error in the source code")

    imports = {}
    used_names = set()

    # Collect imports and their aliases
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports[alias.name] = alias.asname or alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:  # Only consider top-level imports
                for alias in node.names:
                    imports[alias.name] = alias.asname or alias.name

    # Collect used names
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used_names.add(node.id)

    # Determine unused imports
    unused = []
    for original_name, alias in imports.items():
        if alias not in used_names:
            unused.append(original_name)

    return unused
