import ast

def estimate_complexity(func_source: str) -> dict:
    if not func_source.strip():
        raise ValueError("Source code cannot be empty.")
    
    try:
        # Parse the source code into an AST
        tree = ast.parse(func_source)
    except SyntaxError:
        raise ValueError("Source code cannot be parsed.")
    
    # Check for exactly one top-level function
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    if len(functions) != 1:
        raise ValueError("Source code must define exactly one top-level function.")
    
    function_node = functions[0]
    
    # Count non-blank lines
    lines = sum(1 for line in func_source.splitlines() if line.strip())
    
    # Count branches and returns
    branches = 0
    returns = 0
    
    for node in ast.walk(function_node):
        if isinstance(node, ast.If):
            branches += 1  # Count the if statement
            branches += len(node.orelse)  # Count elifs (each elif is a separate node)
        elif isinstance(node, ast.For) or isinstance(node, ast.While):
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
