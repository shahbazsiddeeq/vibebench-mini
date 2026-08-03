import ast
from typing import List, Tuple


def find_untyped_functions(source: str) -> List[Tuple[str, int]]:
    """
    Parse Python source and return list of (function_name, lineno) tuples
    for functions missing at least one required type annotation.
    
    A function is fully annotated when:
    - It has a return annotation (-> T)
    - Every parameter is annotated, except:
      - The first parameter of a method (function in class body) if named 'self' or 'cls'
    
    Parameters checked: positional-only, ordinary, keyword-only, *args, **kwargs
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}")
    
    untyped = []
    
    class FunctionVisitor(ast.NodeVisitor):
        def __init__(self):
            self.class_depth = 0
        
        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            self.class_depth += 1
            self.generic_visit(node)
            self.class_depth -= 1
        
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self._check_function(node)
            self.generic_visit(node)
        
        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            self._check_function(node)
            self.generic_visit(node)
        
        def _check_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
            # Check if function is fully annotated
            is_method = self.class_depth > 0
            
            # Check return annotation
            has_return_annotation = node.returns is not None
            
            # Check parameter annotations
            args = node.args
            all_params_annotated = True
            
            # Check positional-only parameters
            for i, arg in enumerate(args.posonlyargs):
                if arg.annotation is None:
                    all_params_annotated = False
                    break
            
            # Check ordinary parameters
            if all_params_annotated:
                for i, arg in enumerate(args.args):
                    # First parameter of method can be exempt if named 'self' or 'cls'
                    if is_method and i == 0 and arg.arg in ('self', 'cls'):
                        continue
                    if arg.annotation is None:
                        all_params_annotated = False
                        break
            
            # Check keyword-only parameters
            if all_params_annotated:
                for arg in args.kwonlyargs:
                    if arg.annotation is None:
                        all_params_annotated = False
                        break
            
            # Check *args parameter
            if all_params_annotated and args.vararg is not None:
                if args.vararg.annotation is None:
                    all_params_annotated = False
            
            # Check **kwargs parameter
            if all_params_annotated and args.kwarg is not None:
                if args.kwarg.annotation is None:
                    all_params_annotated = False
            
            # Report if missing annotations
            if not has_return_annotation or not all_params_annotated:
                untyped.append((node.name, node.lineno))
    
    visitor = FunctionVisitor()
    visitor.visit(tree)
    
    # Sort by (lineno, function_name)
    untyped.sort(key=lambda x: (x[1], x[0]))
    
    return untyped
