import ast
from typing import List, Tuple


def find_untyped_functions(source: str) -> List[Tuple[str, int]]:
    """
    Find all function definitions missing at least one required type annotation.
    
    A function is fully annotated when:
    - It has a return annotation (-> T)
    - Every parameter is annotated
    
    Exception: The first parameter of a method (function directly in a class body)
    named 'self' or 'cls' is exempt from annotation requirement.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}")
    
    untyped = []
    
    def is_method_in_class(node: ast.FunctionDef, parent_is_class: bool) -> bool:
        """Check if this function is a direct method of a class."""
        return parent_is_class
    
    def check_function(node: ast.FunctionDef, parent_is_class: bool) -> None:
        """Check if a function is missing annotations."""
        # Determine if this is a method (directly in a class)
        is_method = parent_is_class
        
        # Check return annotation
        has_return_annotation = node.returns is not None
        
        # Check parameters
        args = node.args
        missing_param_annotation = False
        
        # Check positional-only parameters
        for i, arg in enumerate(args.posonlyargs):
            if arg.annotation is None:
                # First param of method with name 'self' or 'cls' is exempt
                if is_method and i == 0 and arg.arg in ('self', 'cls'):
                    continue
                missing_param_annotation = True
                break
        
        # Check regular positional/keyword parameters
        if not missing_param_annotation:
            for i, arg in enumerate(args.args):
                if arg.annotation is None:
                    # First param of method with name 'self' or 'cls' is exempt
                    # Note: if there are posonlyargs, they come first, so we need to account for that
                    param_index = len(args.posonlyargs) + i
                    if is_method and param_index == 0 and arg.arg in ('self', 'cls'):
                        continue
                    missing_param_annotation = True
                    break
        
        # Check *args parameter
        if not missing_param_annotation and args.vararg is not None:
            if args.vararg.annotation is None:
                missing_param_annotation = True
        
        # Check keyword-only parameters
        if not missing_param_annotation:
            for arg in args.kwonlyargs:
                if arg.annotation is None:
                    missing_param_annotation = True
                    break
        
        # Check **kwargs parameter
        if not missing_param_annotation and args.kwarg is not None:
            if args.kwarg.annotation is None:
                missing_param_annotation = True
        
        # Report if missing annotations
        if not has_return_annotation or missing_param_annotation:
            untyped.append((node.name, node.lineno))
    
    def visit(node: ast.AST, parent_is_class: bool = False) -> None:
        """Recursively visit nodes and check functions."""
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            check_function(node, parent_is_class)
            # Visit nested functions/classes inside this function
            # Nested functions are NOT methods (parent_is_class = False)
            for child in ast.iter_child_nodes(node):
                visit(child, parent_is_class=False)
        elif isinstance(node, ast.ClassDef):
            # Visit methods in the class (parent_is_class = True)
            for child in ast.iter_child_nodes(node):
                visit(child, parent_is_class=True)
        else:
            # Visit other nodes normally
            for child in ast.iter_child_nodes(node):
                visit(child, parent_is_class=parent_is_class)
    
    visit(tree)
    
    # Sort by line number, then by function name
    untyped.sort(key=lambda x: (x[1], x[0]))
    
    return untyped
