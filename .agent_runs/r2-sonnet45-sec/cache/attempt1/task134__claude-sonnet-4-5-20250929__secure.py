import ast
import re


def non_snake_case_functions(source: str) -> list[str]:
    """
    Parse source code and return function names that don't match snake_case pattern.
    
    Returns function names in source order (by line then column) that don't match
    the pattern ^[a-z_][a-z0-9_]*$.
    
    Args:
        source: Python source code as a string
        
    Returns:
        List of function names that are not in snake_case
        
    Raises:
        ValueError: If source has syntax errors
    """
    # Validate input
    if not isinstance(source, str):
        raise ValueError("Source must be a string")
    
    # Pattern for valid snake_case names
    snake_case_pattern = re.compile(r'^[a-z_][a-z0-9_]*$')
    
    # Parse the source code
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Syntax error in source code: {e}")
    
    # Collect all function definitions with their positions
    non_snake_case_names = []
    
    class FunctionVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            # Check if the function name matches snake_case pattern
            if not snake_case_pattern.match(node.name):
                non_snake_case_names.append((node.lineno, node.col_offset, node.name))
            # Continue visiting nested functions
            self.generic_visit(node)
        
        def visit_AsyncFunctionDef(self, node):
            # Check if the async function name matches snake_case pattern
            if not snake_case_pattern.match(node.name):
                non_snake_case_names.append((node.lineno, node.col_offset, node.name))
            # Continue visiting nested functions
            self.generic_visit(node)
    
    visitor = FunctionVisitor()
    visitor.visit(tree)
    
    # Sort by line number, then column offset, and extract just the names
    non_snake_case_names.sort(key=lambda x: (x[0], x[1]))
    
    return [name for _, _, name in non_snake_case_names]
