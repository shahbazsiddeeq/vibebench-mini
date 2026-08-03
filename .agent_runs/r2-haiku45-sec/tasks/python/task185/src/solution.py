import ast
from typing import List, Tuple


def find_mutable_defaults(source: str) -> List[Tuple[str, int]]:
    """
    Parse Python source code and find functions with mutable default arguments.
    
    Returns a list of tuples (function_name, lineno) for each function that has
    at least one mutable default argument (list, dict, or set literal displays).
    Results are sorted by (lineno, function_name).
    
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
    
    # Collect functions with mutable defaults
    functions_with_mutable_defaults = set()
    
    class FunctionVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self._check_function(node)
            self.generic_visit(node)
        
        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            self._check_function(node)
            self.generic_visit(node)
        
        def _check_function(self, node) -> None:
            """Check if a function has mutable defaults."""
            has_mutable_default = False
            
            # Check regular defaults
            for default in node.args.defaults:
                if self._is_mutable_default(default):
                    has_mutable_default = True
                    break
            
            # Check keyword-only defaults
            if not has_mutable_default:
                for default in node.args.kw_defaults:
                    if default is not None and self._is_mutable_default(default):
                        has_mutable_default = True
                        break
            
            if has_mutable_default:
                functions_with_mutable_defaults.add((node.name, node.lineno))
        
        @staticmethod
        def _is_mutable_default(node: ast.expr) -> bool:
            """
            Check if a default value is a mutable literal display.
            
            Returns True for:
            - List displays: [], [1, 2], etc.
            - Dict displays: {}, {1: 2}, etc.
            - Set displays: {1, 2}, etc.
            
            Returns False for:
            - Tuple displays
            - Constants (strings, numbers, None, bool)
            - Function calls (list(), dict(), etc.)
            - Other expressions
            """
            if isinstance(node, ast.List):
                return True
            if isinstance(node, ast.Dict):
                return True
            if isinstance(node, ast.Set):
                return True
            return False
    
    visitor = FunctionVisitor()
    visitor.visit(tree)
    
    # Sort by lineno first, then by function name
    result = sorted(functions_with_mutable_defaults, key=lambda x: (x[1], x[0]))
    
    return result
