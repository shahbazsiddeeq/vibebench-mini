import ast
import re


def non_snake_case_functions(source):
    """
    Parse source code and return names of function definitions that don't match
    snake_case pattern (^[a-z_][a-z0-9_]*$), in source order.
    
    Includes top-level functions, nested functions, async functions, and methods.
    Excludes class names and dunder methods.
    
    Raises ValueError on syntax errors.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Syntax error: {e}")
    
    snake_case_pattern = re.compile(r'^[a-z_][a-z0-9_]*$')
    non_snake_case = []
    
    def is_dunder(name):
        """Check if a name is a dunder method (starts and ends with __)"""
        return name.startswith('__') and name.endswith('__')
    
    def is_snake_case(name):
        """Check if a name matches snake_case pattern"""
        return bool(snake_case_pattern.match(name))
    
    def visit_node(node):
        """Recursively visit nodes and collect non-snake-case function names"""
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Skip dunder methods
            if not is_dunder(node.name):
                # Check if name is not snake_case
                if not is_snake_case(node.name):
                    non_snake_case.append(node.name)
            
            # Visit nested functions in the body
            for child in node.body:
                visit_node(child)
        
        elif isinstance(node, ast.ClassDef):
            # Visit methods inside the class (but don't report the class name itself)
            for child in node.body:
                visit_node(child)
        
        elif isinstance(node, (ast.Module, ast.If, ast.For, ast.While, ast.With, 
                               ast.Try, ast.ExceptHandler)):
            # Visit children of container nodes
            for child in ast.iter_child_nodes(node):
                visit_node(child)
    
    visit_node(tree)
    return non_snake_case
