import ast


def estimate_complexity(func_source: str) -> dict:
    """
    Estimate the complexity of a Python function by counting lines, branches, and returns.
    
    Args:
        func_source: Source code of a single Python function
        
    Returns:
        Dictionary with keys "lines", "branches", "returns"
        
    Raises:
        ValueError: If source is empty, cannot be parsed, or doesn't define exactly one function
    """
    # Validate input is not empty
    if not func_source or not func_source.strip():
        raise ValueError("Source code is empty")
    
    # Parse the source code
    try:
        tree = ast.parse(func_source)
    except SyntaxError as e:
        raise ValueError(f"Cannot parse source code") from e
    
    # Validate exactly one top-level function definition
    top_level_funcs = [node for node in tree.body if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef)]
    
    if len(top_level_funcs) != 1:
        raise ValueError("Source must define exactly one top-level function")
    
    # Check that there are no other top-level statements
    if len(tree.body) != 1:
        raise ValueError("Source must define exactly one top-level function")
    
    func_node = top_level_funcs[0]
    
    # Count non-blank lines
    lines = sum(1 for line in func_source.split('\n') if line.strip())
    
    # Count branches and returns using AST visitor
    branch_count = 0
    return_count = 0
    
    for node in ast.walk(func_node):
        if isinstance(node, ast.If):
            branch_count += 1
        elif isinstance(node, ast.For):
            branch_count += 1
        elif isinstance(node, ast.While):
            branch_count += 1
        elif isinstance(node, ast.ExceptHandler):
            branch_count += 1
        elif isinstance(node, ast.Return):
            return_count += 1
    
    return {
        "lines": lines,
        "branches": branch_count,
        "returns": return_count
    }
