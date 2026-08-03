import ast
from typing import List, Tuple


def find_mutable_defaults(source: str) -> List[Tuple[str, int]]:
    """
    Parse Python source code and find functions with mutable default arguments.
    
    Returns a list of tuples (function_name, lineno) for each function that has
    at least one mutable default argument (list, dict, or set literal displays).
    Results are sorted by (lineno, function_name).
    
    Raises ValueError if source is not valid Python.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}")
    
    results = []
    
    def has_mutable_default(node: ast.AST) -> bool:
        """Check if an AST node is a mutable literal display."""
        return isinstance(node, (ast.List, ast.Dict, ast.Set))
    
    def check_function(func_node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        """Check if a function has mutable defaults and add to results if so."""
        # Check regular defaults
        for default in func_node.args.defaults:
            if has_mutable_default(default):
                results.append((func_node.name, func_node.lineno))
                return
        
        # Check keyword-only defaults
        for default in func_node.args.kw_defaults:
            if default is not None and has_mutable_default(default):
                results.append((func_node.name, func_node.lineno))
                return
    
    def visit_node(node: ast.AST) -> None:
        """Recursively visit all nodes and check function definitions."""
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            check_function(node)
        
        # Recursively visit child nodes
        for child in ast.iter_child_nodes(node):
            visit_node(child)
    
    visit_node(tree)
    
    # Sort by lineno first, then by function_name
    results.sort(key=lambda x: (x[1], x[0]))
    
    return results
