import ast

def non_snake_case_functions(source: str) -> list:
    # Parse the source code into an AST
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Syntax error in source code: {e}")

    # Define a function to check if a name is in snake_case
    def is_snake_case(name: str) -> bool:
        return bool(name) and name[0].islower() and all(c.isalnum() or c == '_' for c in name) and not name.startswith('_')

    # List to hold non-snake-case function names
    non_snake_case_names = []

    # Define a visitor class to traverse the AST
    class FunctionVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            if not is_snake_case(node.name) and not node.name.startswith('__'):
                non_snake_case_names.append(node.name)
            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            if not is_snake_case(node.name):
                non_snake_case_names.append(node.name)
            self.generic_visit(node)

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            self.generic_visit(node)

    # Create a visitor instance and visit the tree
    visitor = FunctionVisitor()
    visitor.visit(tree)

    return non_snake_case_names
