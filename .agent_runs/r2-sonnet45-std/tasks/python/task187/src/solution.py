import ast


def find_bare_excepts(source: str) -> list[int]:
    """
    Parse Python source and return sorted list of line numbers of bare except clauses.
    
    A bare except clause is an ast.ExceptHandler with type=None (written as `except:`).
    
    Args:
        source: Python source code as a string
        
    Returns:
        Sorted list of 1-based line numbers where bare except clauses appear
        
    Raises:
        ValueError: If source is not valid Python
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}")
    
    class BareExceptVisitor(ast.NodeVisitor):
        def __init__(self):
            self.bare_except_lines = []
        
        def visit_ExceptHandler(self, node):
            # Check if this is a bare except (type is None)
            if node.type is None:
                self.bare_except_lines.append(node.lineno)
            # Continue visiting child nodes
            self.generic_visit(node)
    
    visitor = BareExceptVisitor()
    visitor.visit(tree)
    
    return sorted(visitor.bare_except_lines)
