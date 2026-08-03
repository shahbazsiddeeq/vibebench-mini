import ast

def find_bare_excepts(source: str) -> list[int]:
    # Validate the input source code
    if not isinstance(source, str):
        raise ValueError("Source must be a string.")
    
    try:
        # Parse the source code into an AST
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid Python source code.")

    bare_except_lines = []

    # Define a visitor class to find bare except clauses
    class ExceptVisitor(ast.NodeVisitor):
        def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
            # Check if the type is None (bare except)
            if node.type is None:
                bare_except_lines.append(node.lineno)
            # Continue visiting other nodes
            self.generic_visit(node)

    # Create an instance of the visitor and visit the AST
    visitor = ExceptVisitor()
    visitor.visit(tree)

    # Return the sorted list of line numbers
    return sorted(bare_except_lines)
