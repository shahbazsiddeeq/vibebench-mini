import ast
from typing import List, Tuple


def compute_complexity(source: str) -> List[Tuple[str, int, int]]:
    """
    Compute cyclomatic complexity for all functions in source code.
    
    Returns list of (function_name, lineno, complexity) tuples sorted by (lineno, function_name).
    Raises ValueError if source is not valid Python.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}")
    
    results = []
    
    def visit_function(node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        """Visit a function definition and compute its complexity."""
        complexity = 1  # Base complexity
        
        # Walk through the function's own body (not nested functions/classes)
        for child in ast.walk(node):
            # Skip nodes that are inside nested functions, async functions, lambdas, or classes
            if child is not node and isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
                continue
            
            # Only count direct descendants of this function's body
            if not _is_in_function_body(node, child):
                continue
            
            # Count decision points
            if isinstance(child, ast.If):
                complexity += 1
            elif isinstance(child, (ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.While):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.IfExp):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                # Each boolean operator adds (number of operands - 1)
                complexity += len(child.values) - 1
        
        # Count comprehension if-clauses
        for child in ast.walk(node):
            if child is not node and isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
                continue
            if not _is_in_function_body(node, child):
                continue
            
            # Check for comprehensions (ListComp, SetComp, DictComp, GeneratorExp)
            if isinstance(child, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                # Count if-clauses in generators
                for generator in child.generators:
                    complexity += len(generator.ifs)
        
        results.append((node.name, node.lineno, complexity))
        
        # Visit nested functions
        for child in node.body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                visit_function(child)
            elif isinstance(child, ast.ClassDef):
                # Visit methods inside classes
                for class_child in child.body:
                    if isinstance(class_child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        visit_function(class_child)
    
    # Find all top-level functions and classes
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            visit_function(node)
        elif isinstance(node, ast.ClassDef):
            # Visit methods inside top-level classes
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    visit_function(child)
    
    # Sort by lineno, then by function_name
    results.sort(key=lambda x: (x[1], x[0]))
    
    return results


def _is_in_function_body(func_node: ast.FunctionDef | ast.AsyncFunctionDef, target: ast.AST) -> bool:
    """
    Check if target node is directly in the function body (not in nested functions/classes/lambdas).
    """
    for node in ast.walk(func_node):
        if node is target:
            # Now check if target is inside a nested function/class/lambda
            for parent in ast.walk(func_node):
                if parent is func_node:
                    continue
                if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
                    # Check if target is inside this nested structure
                    for child in ast.walk(parent):
                        if child is target:
                            return False
            return True
    return False
