import ast
from typing import List, Tuple


def find_mutable_defaults(source: str) -> List[Tuple[str, int]]:
    """
    Find functions with mutable default arguments.
    
    Args:
        source: Python source code as a string
        
    Returns:
        List of (function_name, line_number) tuples sorted by line then name
        
    Raises:
        ValueError: If source is not valid Python
    """
    # Validate input
    if not isinstance(source, str):
        raise ValueError("Source must be a string")
    
    # Parse the source code
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}")
    
    results = []
    
    # Walk through all nodes in the AST
    for node in ast.walk(tree):
        # Check both regular function definitions and async function definitions
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Check if this function has any mutable defaults
            if has_mutable_default(node):
                results.append((node.name, node.lineno))
    
    # Sort by line number first, then by function name
    results.sort(key=lambda x: (x[1], x[0]))
    
    return results


def has_mutable_default(func_node: ast.FunctionDef) -> bool:
    """
    Check if a function has any mutable literal default arguments.
    
    Args:
        func_node: AST node for a function definition
        
    Returns:
        True if the function has at least one mutable default
    """
    args = func_node.args
    
    # Check regular defaults (positional and keyword arguments)
    if args.defaults:
        for default in args.defaults:
            if is_mutable_literal(default):
                return True
    
    # Check keyword-only defaults
    if args.kw_defaults:
        for default in args.kw_defaults:
            # kw_defaults can contain None for arguments without defaults
            if default is not None and is_mutable_literal(default):
                return True
    
    return False


def is_mutable_literal(node: ast.AST) -> bool:
    """
    Check if an AST node represents a mutable literal display.
    
    Only list displays ([]), dict displays ({}), and set displays ({1, 2})
    count as mutable literals. Calls like list() or dict() do not count.
    
    Args:
        node: AST node to check
        
    Returns:
        True if the node is a mutable literal display
    """
    # List display: []
    if isinstance(node, ast.List):
        return True
    
    # Dict display: {}
    if isinstance(node, ast.Dict):
        return True
    
    # Set display: {1, 2}
    if isinstance(node, ast.Set):
        return True
    
    return False
