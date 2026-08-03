import ast


def find_mutable_defaults(source: str) -> list[tuple[str, int]]:
    """
    Find functions with mutable default arguments.
    
    Returns a list of (function_name, lineno) tuples for functions that have
    at least one parameter with a mutable literal default (list, dict, or set display).
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}")
    
    results = []
    
    def is_mutable_default(node):
        """Check if an AST node represents a mutable literal default."""
        # List display: []
        if isinstance(node, ast.List):
            return True
        # Dict display: {}
        if isinstance(node, ast.Dict):
            return True
        # Set display: {1, 2, ...}
        if isinstance(node, ast.Set):
            return True
        return False
    
    def visit_function(node):
        """Check if a function has any mutable defaults."""
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return False
        
        # Check regular defaults (positional/keyword arguments)
        if node.args.defaults:
            for default in node.args.defaults:
                if is_mutable_default(default):
                    return True
        
        # Check keyword-only defaults
        if node.args.kw_defaults:
            for default in node.args.kw_defaults:
                # kw_defaults can contain None for args without defaults
                if default is not None and is_mutable_default(default):
                    return True
        
        return False
    
    def traverse(node):
        """Recursively traverse the AST to find all function definitions."""
        for child in ast.walk(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if visit_function(child):
                    results.append((child.name, child.lineno))
    
    traverse(tree)
    
    # Sort by line number, then by function name
    results.sort(key=lambda x: (x[1], x[0]))
    
    return results
