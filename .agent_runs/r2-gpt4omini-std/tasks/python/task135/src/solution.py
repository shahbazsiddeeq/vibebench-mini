import ast

def unused_imports(source):
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Syntax error in the provided source code.")

    imports = {}
    used_names = set()

    # Collect all import statements and their bound names
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports[alias.name] = alias.asname if alias.asname else alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module is not None and node.level == 0:
                for alias in node.names:
                    imports[alias.name] = alias.asname if alias.asname else alias.name
        elif isinstance(node, ast.Name):
            used_names.add(node.id)

    # Determine unused imports
    unused = []
    for name, alias in imports.items():
        if alias not in used_names:
            unused.append(alias)

    return unused
