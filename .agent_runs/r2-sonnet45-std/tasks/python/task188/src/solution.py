import ast


def find_untyped_functions(source: str) -> list[tuple[str, int]]:
    """
    Find all function definitions missing required type annotations.
    
    Returns a list of (function_name, lineno) tuples for functions that are
    missing at least one required annotation, sorted by (lineno, function_name).
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}")
    
    untyped = []
    
    def is_method(node, parent):
        """Check if a function node is a method (direct child of a class)."""
        return isinstance(parent, ast.ClassDef)
    
    def should_exempt_first_param(func_node, parent):
        """
        Check if the first parameter should be exempt from annotation requirement.
        Only exempt if it's a method (direct child of class) and named 'self' or 'cls'.
        """
        if not is_method(func_node, parent):
            return False
        
        args = func_node.args
        # Check if there's at least one parameter
        first_param = None
        
        # Check positional-only parameters first
        if args.posonlyargs:
            first_param = args.posonlyargs[0]
        # Then regular args
        elif args.args:
            first_param = args.args[0]
        
        if first_param and first_param.arg in ('self', 'cls'):
            return True
        
        return False
    
    def is_fully_annotated(func_node, parent):
        """Check if a function is fully annotated."""
        # Must have return annotation
        if func_node.returns is None:
            return False
        
        args = func_node.args
        exempt_first = should_exempt_first_param(func_node, parent)
        
        # Check positional-only parameters
        for i, arg in enumerate(args.posonlyargs):
            if exempt_first and i == 0:
                continue
            if arg.annotation is None:
                return False
        
        # Check regular positional/keyword parameters
        start_idx = 0
        if exempt_first and not args.posonlyargs:
            start_idx = 1
        
        for i, arg in enumerate(args.args):
            if i < start_idx:
                continue
            if arg.annotation is None:
                return False
        
        # Check keyword-only parameters
        for arg in args.kwonlyargs:
            if arg.annotation is None:
                return False
        
        # Check *args
        if args.vararg is not None and args.vararg.annotation is None:
            return False
        
        # Check **kwargs
        if args.kwarg is not None and args.kwarg.annotation is None:
            return False
        
        return True
    
    def visit_node(node, parent=None):
        """Recursively visit AST nodes to find function definitions."""
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not is_fully_annotated(node, parent):
                untyped.append((node.name, node.lineno))
            
            # Visit children with this function as parent
            for child in ast.iter_child_nodes(node):
                visit_node(child, node)
        elif isinstance(node, ast.ClassDef):
            # Visit children with this class as parent
            for child in ast.iter_child_nodes(node):
                visit_node(child, node)
        else:
            # For other nodes, continue traversal
            for child in ast.iter_child_nodes(node):
                visit_node(child, parent)
    
    visit_node(tree)
    
    # Sort by (lineno, function_name)
    untyped.sort(key=lambda x: (x[1], x[0]))
    
    return untyped
