import ast
from typing import List


def unused_imports(source: str) -> List[str]:
    """
    Parse source code and return a list of imported names that are never used.
    
    - Parses source with ast
    - Returns bound names from import/from-import statements that are never referenced
    - A reference only counts if it appears as a real Name node in the code
    - Names in string literals or comments do NOT count as usage
    - For 'import a as b', the alias 'b' is what's bound
    - For 'import a.b.c', only 'a' is bound
    - 'from m import *' binds no inspectable name and is never reported
    - Returns names in source order
    - Raises ValueError on syntax errors
    
    Args:
        source: Python source code as a string
        
    Returns:
        List of unused import names in source order
        
    Raises:
        ValueError: If source has syntax errors
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Syntax error in source: {e}")
    
    # Track imported names and their line numbers for ordering
    imported_names = {}  # name -> line_number
    
    # Collect all imported names
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                # For 'import a.b.c', only 'a' is bound
                # For 'import a as b', 'b' is bound
                name = alias.asname if alias.asname else alias.name.split('.')[0]
                imported_names[name] = node.lineno
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                # Skip star imports - they bind no inspectable name
                if alias.name == '*':
                    continue
                # For 'from m import a as b', 'b' is bound
                # For 'from m import a', 'a' is bound
                name = alias.asname if alias.asname else alias.name
                imported_names[name] = node.lineno
    
    # Collect all Name nodes that are actually used in the code
    # (excluding those in Import/ImportFrom statements themselves)
    used_names = set()
    
    for node in ast.walk(tree):
        # Skip Import and ImportFrom nodes themselves
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        # Collect all Name nodes that are loaded (used)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used_names.add(node.id)
    
    # Find unused imports in source order
    unused = []
    for name in sorted(imported_names.keys(), key=lambda x: imported_names[x]):
        if name not in used_names:
            unused.append(name)
    
    return unused
