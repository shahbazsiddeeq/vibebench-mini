import ast

def estimate_complexity(func_source: str) -> dict:
    if not func_source.strip():
        raise ValueError("Source code is empty")

    try:
        tree = ast.parse(func_source)
    except SyntaxError:
        raise ValueError("Source code cannot be parsed")

    # Check for exactly one top-level function
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    if len(functions) != 1:
        raise ValueError("Source code must define exactly one top-level function")

    function_node = functions[0]
    
    lines = sum(1 for line in func_source.splitlines() if line.strip())
    branches = sum(isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler)) for node in ast.walk(function_node))
    returns = sum(isinstance(node, ast.Return) for node in ast.walk(function_node))

    return {
        "lines": lines,
        "branches": branches,
        "returns": returns
    }
