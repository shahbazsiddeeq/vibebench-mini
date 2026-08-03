import ast
from typing import List, Tuple


def compute_complexity(source: str) -> List[Tuple[str, int, int]]:
    """
    Compute cyclomatic complexity for all functions in Python source code.
    
    Returns a list of tuples (function_name, lineno, complexity) sorted by
    (lineno, function_name).
    
    Raises ValueError if source is not valid Python.
    """
    # Validate input
    if not isinstance(source, str):
        raise ValueError("source must be a string")
    
    # Parse the source code
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}")
    
    results = []
    
    # Walk through the AST and find all function definitions
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            complexity = _compute_function_complexity(node)
            results.append((node.name, node.lineno, complexity))
    
    # Sort by lineno first, then by function name
    results.sort(key=lambda x: (x[1], x[0]))
    
    return results


def _compute_function_complexity(func_node: ast.AST) -> int:
    """
    Compute complexity for a single function node.
    Only counts decision points in the function's own body, not nested functions.
    """
    complexity = 1  # Base complexity
    
    # Process the function body
    for stmt in func_node.body:
        complexity += _count_complexity_in_node(stmt, skip_nested_defs=True)
    
    return complexity


def _count_complexity_in_node(node: ast.AST, skip_nested_defs: bool = False) -> int:
    """
    Count complexity contributions in a node.
    
    If skip_nested_defs is True, don't recurse into nested function/class definitions.
    """
    complexity = 0
    
    # If this is a nested function/class definition and we should skip it, return 0
    if skip_nested_defs and isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
        return 0
    
    # Count decision points
    if isinstance(node, ast.If):
        complexity += 1
    elif isinstance(node, (ast.For, ast.AsyncFor)):
        complexity += 1
    elif isinstance(node, ast.While):
        complexity += 1
    elif isinstance(node, ast.ExceptHandler):
        complexity += 1
    elif isinstance(node, ast.IfExp):
        # Ternary expression
        complexity += 1
    elif isinstance(node, ast.BoolOp):
        # Boolean operation (and/or): add (number of operands - 1)
        complexity += len(node.values) - 1
    
    # Recurse into child nodes, but skip nested function/class definitions
    for child in ast.iter_child_nodes(node):
        if skip_nested_defs and isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            continue
        complexity += _count_complexity_in_node(child, skip_nested_defs=skip_nested_defs)
    
    return complexity
