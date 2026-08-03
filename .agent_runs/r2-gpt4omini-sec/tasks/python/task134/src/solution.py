import ast
import re

def non_snake_case_functions(source: str) -> list:
    # Validate input
    if not isinstance(source, str):
        raise ValueError("Input must be a string.")

    # Regular expression for snake_case
    snake_case_pattern = re.compile(r'^[a-z_][a-z0-9_]*$')

    # List to hold non-snake-case function names
    non_snake_case_names = []

    try:
        # Parse the source code into an AST
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Syntax error in source code: {e}")

    # Function to check for non-snake-case names
    def check_function_names(node):
        if isinstance(node, ast.FunctionDef):
            if not snake_case_pattern.match(node.name) and not node.name.startswith('__'):
                non_snake_case_names.append(node.name)
        elif isinstance(node, ast.AsyncFunctionDef):
            if not snake_case_pattern.match(node.name) and not node.name.startswith('__'):
                non_snake_case_names.append(node.name)
        # Recursively check nested functions
        for child in ast.iter_child_nodes(node):
            check_function_names(child)

    # Start checking from the root of the AST
    check_function_names(tree)

    return non_snake_case_names
