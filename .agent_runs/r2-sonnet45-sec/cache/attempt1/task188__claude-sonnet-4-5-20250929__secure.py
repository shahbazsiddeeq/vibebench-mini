import ast
from typing import List, Tuple


def find_untyped_functions(source: str) -> List[Tuple[str, int]]:
    """
    Find all functions missing required type annotations.
    
    Args:
        source: Python source code as a string
        
    Returns:
        List of (function_name, lineno) tuples for functions missing annotations,
        sorted by (lineno, function_name)
        
    Raises:
        ValueError: If source is not valid Python
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}")
    
    untyped_functions = []
    
    def is_method(node: ast.FunctionDef, parent) -> bool:
        """Check if a function is a method (directly in a class body)."""
        return isinstance(parent, ast.ClassDef)
    
    def check_function(node: ast.FunctionDef, parent) -> bool:
        """
        Check if a function is fully annotated.
        Returns True if missing annotations, False if fully annotated.
        """
        # Check return annotation
        if node.returns is None:
            return True
        
        args = node.args
        
        # Determine if first parameter should be exempt
        first_param_exempt = False
        if is_method(node, parent):
            # Check if there's at least one parameter
            all_params = []
            if args.posonlyargs:
                all_params.extend(args.posonlyargs)
            if args.args:
                all_params.extend(args.args)
            
            if all_params:
                first_param = all_params[0]
                if first_param.arg in ('self', 'cls'):
                    first_param_exempt = True
        
        # Check positional-only parameters
        for i, arg in enumerate(args.posonlyargs):
            # Skip first param if exempt
            if i == 0 and first_param_exempt and not args.args:
                continue
            if arg.annotation is None:
                return True
        
        # Check regular positional parameters
        start_idx = 0
        if first_param_exempt and args.posonlyargs:
            # First param was in posonlyargs, so no exemption here
            start_idx = 0
        elif first_param_exempt and args.args:
            # First param is in args and is exempt
            start_idx = 1
        
        for i, arg in enumerate(args.args):
            if i < start_idx:
                continue
            if arg.annotation is None:
                return True
        
        # Check *args
        if args.vararg is not None and args.vararg.annotation is None:
            return True
        
        # Check keyword-only parameters
        for arg in args.kwonlyargs:
            if arg.annotation is None:
                return True
        
        # Check **kwargs
        if args.kwarg is not None and args.kwarg.annotation is None:
            return True
        
        return False
    
    def visit_node(node, parent=None):
        """Recursively visit AST nodes to find function definitions."""
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if check_function(node, parent):
                untyped_functions.append((node.name, node.lineno))
            # Continue visiting children with this function as parent
            for child in ast.iter_child_nodes(node):
                visit_node(child, node)
        elif isinstance(node, ast.ClassDef):
            # Visit class body with class as parent
            for child in ast.iter_child_nodes(node):
                visit_node(child, node)
        else:
            # For other nodes, continue with same parent
            for child in ast.iter_child_nodes(node):
                visit_node(child, parent)
    
    visit_node(tree)
    
    # Sort by (lineno, function_name)
    untyped_functions.sort(key=lambda x: (x[1], x[0]))
    
    return untyped_functions
