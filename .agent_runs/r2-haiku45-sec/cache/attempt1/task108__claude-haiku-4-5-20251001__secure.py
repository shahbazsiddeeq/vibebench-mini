import ast
from typing import Dict


def estimate_complexity(func_source: str) -> Dict[str, int]:
    """
    Estimate the complexity of a Python function by analyzing its source code.
    
    Args:
        func_source: Source code string containing exactly one function definition
        
    Returns:
        Dictionary with keys "lines", "branches", and "returns" containing counts
        
    Raises:
        ValueError: If source is empty, cannot be parsed, or doesn't define exactly one function
    """
    # Validate input
    if not func_source or not isinstance(func_source, str):
        raise ValueError("Source code must be a non-empty string")
    
    # Try to parse the source code
    try:
        tree = ast.parse(func_source)
    except SyntaxError as e:
        raise ValueError(f"Source code cannot be parsed: {e}")
    
    # Find all top-level function definitions
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    
    # Filter to only top-level functions (direct children of Module)
    top_level_functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    
    # Validate exactly one top-level function
    if len(top_level_functions) != 1:
        raise ValueError("Source code must define exactly one top-level function")
    
    func_node = top_level_functions[0]
    
    # Count non-blank lines
    lines = count_non_blank_lines(func_source)
    
    # Count branches (If, For, While, ExceptHandler)
    branches = count_branches(func_node)
    
    # Count returns
    returns = count_returns(func_node)
    
    return {
        "lines": lines,
        "branches": branches,
        "returns": returns
    }


def count_non_blank_lines(source: str) -> int:
    """Count non-blank lines in source code."""
    lines = source.split('\n')
    non_blank_count = 0
    for line in lines:
        stripped = line.strip()
        if stripped:  # Non-empty after stripping whitespace
            non_blank_count += 1
    return non_blank_count


def count_branches(func_node: ast.FunctionDef) -> int:
    """Count branch points in a function: If, For, While, ExceptHandler."""
    count = 0
    
    for node in ast.walk(func_node):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
            count += 1
    
    return count


def count_returns(func_node: ast.FunctionDef) -> int:
    """Count return statements in a function."""
    count = 0
    
    for node in ast.walk(func_node):
        if isinstance(node, ast.Return):
            count += 1
    
    return count
