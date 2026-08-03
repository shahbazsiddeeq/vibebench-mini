import ast
from typing import List


def unused_imports(source: str) -> List[str]:
    """
    Parse source code and return imported names that are never referenced.
    
    Args:
        source: Python source code as a string
        
    Returns:
        List of unused import names in source order
        
    Raises:
        ValueError: If source has syntax errors
    """
    # Validate input
    if not isinstance(source, str):
        raise ValueError("Source must be a string")
    
    # Parse the source code
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Syntax error in source: {e}")
    
    # Track imported names in order
    imported_names = []  # List of (name, lineno, col_offset) to preserve order
    imported_set = set()  # Set for quick lookup
    
    # Track all Name nodes that reference variables
    used_names = set()
    
    # First pass: collect all imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                # For 'import a.b.c', bind 'a'
                # For 'import x as y', bind 'y'
                if alias.asname:
                    name = alias.asname
                else:
                    # Get the top-level module name
                    name = alias.name.split('.')[0]
                
                if name not in imported_set:
                    imported_names.append((name, node.lineno, node.col_offset))
                    imported_set.add(name)
                    
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                # Skip star imports
                if alias.name == '*':
                    continue
                    
                # For 'from m import x as y', bind 'y'
                # For 'from m import x', bind 'x'
                if alias.asname:
                    name = alias.asname
                else:
                    name = alias.name
                
                if name not in imported_set:
                    imported_names.append((name, node.lineno, node.col_offset))
                    imported_set.add(name)
    
    # Second pass: collect all Name nodes that are loads (references)
    # We need to exclude the import statements themselves
    class NameCollector(ast.NodeVisitor):
        def __init__(self):
            self.used = set()
            self.in_import = False
            
        def visit_Import(self, node):
            # Don't collect names from import statements themselves
            pass
            
        def visit_ImportFrom(self, node):
            # Don't collect names from import statements themselves
            pass
            
        def visit_Name(self, node):
            # Only count Load context (reading the variable)
            # Store context is assignment, Del is deletion
            if isinstance(node.ctx, ast.Load):
                self.used.add(node.id)
            self.generic_visit(node)
    
    collector = NameCollector()
    collector.visit(tree)
    used_names = collector.used
    
    # Find unused imports in original order
    unused = []
    for name, _, _ in imported_names:
        if name not in used_names:
            unused.append(name)
    
    return unused
