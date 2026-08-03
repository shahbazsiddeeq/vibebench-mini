import ast
from typing import List


def unused_imports(source: str) -> List[str]:
    """
    Parse source code and return a list of imported names that are never used.
    
    Returns bound names from import/from-import statements that are never 
    referenced as ast.Name nodes in the source code, in source order.
    
    - For 'import a.b.c', binds 'a'
    - For 'import a as b', binds 'b' (the alias)
    - For 'from m import *', binds nothing (never reported)
    - Names in strings/comments don't count as usage
    
    Raises ValueError on syntax errors.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Syntax error: {e}")
    
    # Track imported names in order: (name, lineno)
    imported_names = {}  # name -> lineno
    import_order = []    # list of names in order
    
    # Track all Name nodes that are actually used (not in strings/comments)
    used_names = set()
    
    # First pass: collect all imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                # 'import a.b.c' binds 'a', 'import a as b' binds 'b'
                bound_name = alias.asname if alias.asname else alias.name.split('.')[0]
                imported_names[bound_name] = node.lineno
                import_order.append(bound_name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                # 'from m import *' binds nothing
                if alias.name == '*':
                    continue
                # 'from m import a as b' binds 'b', 'from m import a' binds 'a'
                bound_name = alias.asname if alias.asname else alias.name
                imported_names[bound_name] = node.lineno
                import_order.append(bound_name)
    
    # Second pass: collect all Name nodes that are actually used
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used_names.add(node.id)
    
    # Return unused imports in source order
    unused = []
    seen = set()
    for name in import_order:
        if name not in seen:
            seen.add(name)
            if name not in used_names:
                unused.append(name)
    
    return unused
