import ast
import re

def non_snake_case_functions(source):
    # Define the regex pattern for snake_case function names
    snake_case_pattern = re.compile(r'^[a-z_][a-z0-9_]*$')

    # Parse the source code into an AST
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError("Invalid syntax") from e

    # List to store non-snake-case function names
    non_snake_case_names = []

    # Define a visitor class to traverse the AST
    class FunctionVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            # Check if the function name matches the snake_case pattern
            if not snake_case_pattern.match(node.name):
                non_snake_case_names.append(node.name)
            # Continue visiting nested functions
            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node):
            # Check if the async function name matches the snake_case pattern
            if not snake_case_pattern.match(node.name):
                non_snake_case_names.append(node.name)
            # Continue visiting nested functions
            self.generic_visit(node)

    # Create an instance of the visitor and visit the AST
    visitor = FunctionVisitor()
    visitor.visit(tree)

    return non_snake_case_names
