import ast


def estimate_complexity(func_source: str) -> dict:
    """
    Estimate the complexity of a Python function.
    
    Returns a dict with:
    - "lines": number of non-blank lines
    - "branches": number of decision points (If, For, While, ExceptHandler)
    - "returns": number of return statements
    
    Raises ValueError if source is empty, cannot be parsed, or doesn't define
    exactly one top-level function.
    """
    if not func_source or not func_source.strip():
        raise ValueError("Source is empty")
    
    # Count non-blank lines
    lines = sum(1 for line in func_source.split('\n') if line.strip())
    
    # Parse the source
    try:
        tree = ast.parse(func_source)
    except SyntaxError:
        raise ValueError("Cannot parse source")
    
    # Check that there's exactly one top-level function definition
    if len(tree.body) != 1:
        raise ValueError("Source must define exactly one top-level function")
    
    if not isinstance(tree.body[0], ast.FunctionDef):
        raise ValueError("Source must define exactly one top-level function")
    
    func_node = tree.body[0]
    
    # Count branches and returns by walking the AST
    branches = 0
    returns = 0
    
    for node in ast.walk(func_node):
        if isinstance(node, (ast.If, ast.For, ast.While)):
            branches += 1
        elif isinstance(node, ast.ExceptHandler):
            branches += 1
        elif isinstance(node, ast.Return):
            returns += 1
    
    return {
        "lines": lines,
        "branches": branches,
        "returns": returns
    }
