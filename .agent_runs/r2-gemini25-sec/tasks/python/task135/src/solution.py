import ast

def unused_imports(source: str) -> list[str]:
    """
    Parses source with ast and returns the bound names from import / from-import
    statements that are never referenced elsewhere as an ast.Name node, in source order.
    A reference only counts if it appears as a real Name in the code; a name that
    appears merely inside a string literal or a comment does NOT count as usage.
    The alias wins for 'as' forms and 'import a.b.c' binds 'a'; a star import
    ('from m import *') binds no inspectable name and is never reported.
    Raises ValueError on syntax errors.
    """
    if not isinstance(source, str):
        raise TypeError("Input 'source' must be a string.")

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Syntax error in source: {e}") from e

    imported_names = []
    used_names = set()

    # First pass: Collect all imported names and their original binding order
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                name_to_bind = alias.asname if alias.asname else alias.name.split('.')[0]
                imported_names.append(name_to_bind)
        elif isinstance(node, ast.ImportFrom):
            if node.names and not (len(node.names) == 1 and node.names[0].name == '*'):
                for alias in node.names:
                    name_to_bind = alias.asname if alias.asname else alias.name
                    imported_names.append(name_to_bind)

    # Second pass: Collect all used names
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Load, ast.Store, ast.Del)):
            used_names.add(node.id)
        elif isinstance(node, ast.Attribute):
            # For attributes like 'os.path', 'os' is the used name
            current_node = node.value
            while isinstance(current_node, ast.Attribute):
                current_node = current_node.value
            if isinstance(current_node, ast.Name) and isinstance(current_node.ctx, (ast.Load, ast.Store, ast.Del)):
                used_names.add(current_node.id)

    # Determine unused imports, maintaining original order
    unused = []
    for name in imported_names:
        if name not in used_names:
            unused.append(name)

    return unused
