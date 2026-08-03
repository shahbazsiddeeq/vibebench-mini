import ast

def unused_imports(source):
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Syntax error in source code")

    # Collect all import names
    import_names = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                import_names[alias.asname or alias.name.split('.')[0]] = node.lineno
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.level == 0:
                for alias in node.names:
                    if alias.name != '*':
                        import_names[alias.asname or alias.name] = node.lineno

    # Collect all used names
    used_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used_names.add(node.id)

    # Determine unused imports
    unused = []
    for name in import_names:
        if name not in used_names:
            unused.append(name)

    # Sort by line number to maintain source order
    unused.sort(key=lambda name: import_names[name])
    return unused
