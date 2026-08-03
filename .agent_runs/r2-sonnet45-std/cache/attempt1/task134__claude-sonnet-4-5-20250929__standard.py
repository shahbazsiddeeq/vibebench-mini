import ast
import re


def non_snake_case_functions(source):
    """
    Parse source code and return function names that don't match snake_case pattern.
    
    Args:
        source: Python source code as a string
        
    Returns:
        List of function names that don't match ^[a-z_][a-z0-9_]*$ in source order
        
    Raises:
        ValueError: If source has syntax errors
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Syntax error: {e}")
    
    # Pattern for valid snake_case
    snake_case_pattern = re.compile(r'^[a-z_][a-z0-9_]*$')
    
    # Collect all function definitions with their positions
    violations = []
    
    class FunctionVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            # Check if the function name matches snake_case
            if not snake_case_pattern.match(node.name):
                violations.append((node.lineno, node.col_offset, node.name))
            # Continue visiting nested functions
            self.generic_visit(node)
        
        def visit_AsyncFunctionDef(self, node):
            # Same check for async functions
            if not snake_case_pattern.match(node.name):
                violations.append((node.lineno, node.col_offset, node.name))
            # Continue visiting nested functions
            self.generic_visit(node)
    
    visitor = FunctionVisitor()
    visitor.visit(tree)
    
    # Sort by line number, then column offset, and extract just the names
    violations.sort(key=lambda x: (x[0], x[1]))
    return [name for _, _, name in violations]
