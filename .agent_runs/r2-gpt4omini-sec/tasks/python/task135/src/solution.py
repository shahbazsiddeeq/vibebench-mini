import ast

def unused_imports(source):
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid syntax in source code")

    imports = {}
    used_names = set()

    # Collect imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports[alias.name] = alias.asname or alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:
                imports[node.module] = None  # Star imports are ignored
        elif isinstance(node, ast.Name):
            used_names.add(node.id)

    # Determine unused imports
    unused = []
    for name, alias in imports.items():
        if alias and alias not in used_names:
            unused.append(alias)
        elif name not in used_names:
            unused.append(name)

    return unused
