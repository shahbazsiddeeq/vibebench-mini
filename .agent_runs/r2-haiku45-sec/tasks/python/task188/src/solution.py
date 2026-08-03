import ast
from typing import List, Tuple


def find_untyped_functions(source: str) -> List[Tuple[str, int]]:
    """
    Parse Python source code and find functions missing type annotations.
    
    A function is fully annotated only when:
    1. It has a return annotation (-> T)
    2. Every parameter is annotated
    
    Exception: The first parameter of a method (function in class body) named
    'self' or 'cls' is exempt from annotation requirement.
    
    Args:
        source: Python source code as a string
        
    Returns:
        List of (function_name, lineno) tuples sorted by (lineno, function_name)
        
    Raises:
        ValueError: If source is not valid Python
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}")
    
    untyped = []
    
    def is_method(node: ast.FunctionDef, parent: ast.AST) -> bool:
        """Check if a function is a method (directly in a class body)."""
        return isinstance(parent, ast.ClassDef)
    
    def check_function(node: ast.FunctionDef, parent: ast.AST) -> bool:
        """
        Check if a function is missing annotations.
        Returns True if function is missing at least one annotation.
        """
        # Check return annotation
        if node.returns is None:
            return True
        
        # Check parameters
        args = node.args
        
        # Collect all parameters that need annotation
        params_to_check = []
        
        # Positional-only parameters
        params_to_check.extend(args.posonlyargs)
        
        # Regular positional/keyword parameters
        params_to_check.extend(args.args)
        
        # Keyword-only parameters
        params_to_check.extend(args.kwonlyargs)
        
        # *args parameter
        if args.vararg is not None:
            params_to_check.append(args.vararg)
        
        # **kwargs parameter
        if args.kwarg is not None:
            params_to_check.append(args.kwarg)
        
        # Check if this is a method and handle 'self'/'cls' exemption
        if is_method(node, parent):
            # The first parameter of a method can be exempt
            if params_to_check:
                first_param = params_to_check[0]
                if first_param.arg in ('self', 'cls'):
                    params_to_check = params_to_check[1:]
        
        # Check if any parameter lacks annotation
        for param in params_to_check:
            if param.annotation is None:
                return True
        
        return False
    
    def visit_node(node: ast.AST, parent: ast.AST) -> None:
        """Recursively visit nodes and check functions."""
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if check_function(node, parent):
                untyped.append((node.name, node.lineno))
            # Continue visiting nested functions
            for child in ast.iter_child_nodes(node):
                visit_node(child, node)
        elif isinstance(node, ast.ClassDef):
            # Visit class body
            for child in node.body:
                visit_node(child, node)
        else:
            # Visit other nodes
            for child in ast.iter_child_nodes(node):
                visit_node(child, node)
    
    # Start visiting from root
    for node in ast.iter_child_nodes(tree):
        visit_node(node, tree)
    
    # Sort by (lineno, function_name)
    untyped.sort(key=lambda x: (x[1], x[0]))
    
    return untyped
