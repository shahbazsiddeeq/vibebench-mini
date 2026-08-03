import ast
import re


def non_snake_case_functions(source: str) -> list[str]:
    """
    Parse source code and return names of function definitions that don't match
    snake_case pattern (^[a-z_][a-z0-9_]*$), in source order.
    
    Includes top-level functions, nested functions, async functions, and methods.
    Excludes class names and dunder methods.
    
    Args:
        source: Python source code as a string
        
    Returns:
        List of function names that don't match snake_case pattern, in source order
        
    Raises:
        ValueError: If source has syntax errors
    """
    if not isinstance(source, str):
        raise ValueError("source must be a string")
    
    # Pattern for valid snake_case: starts with lowercase letter or underscore,
    # followed by lowercase letters, digits, or underscores
    snake_case_pattern = re.compile(r'^[a-z_][a-z0-9_]*$')
    
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Syntax error in source: {e}")
    
    non_snake_case = []
    
    class FunctionVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            # Check if function name matches snake_case pattern
            # Skip dunder methods (names starting and ending with __)
            if not (node.name.startswith('__') and node.name.endswith('__')):
                if not snake_case_pattern.match(node.name):
                    non_snake_case.append((node.lineno, node.col_offset, node.name))
            
            # Continue visiting nested functions
            self.generic_visit(node)
        
        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            # Check if async function name matches snake_case pattern
            # Skip dunder methods
            if not (node.name.startswith('__') and node.name.endswith('__')):
                if not snake_case_pattern.match(node.name):
                    non_snake_case.append((node.lineno, node.col_offset, node.name))
            
            # Continue visiting nested functions
            self.generic_visit(node)
        
        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            # Visit methods inside the class, but don't report the class name itself
            self.generic_visit(node)
    
    visitor = FunctionVisitor()
    visitor.visit(tree)
    
    # Sort by line number, then by column offset to preserve source order
    non_snake_case.sort(key=lambda x: (x[0], x[1]))
    
    # Extract just the names
    return [name for _, _, name in non_snake_case]
