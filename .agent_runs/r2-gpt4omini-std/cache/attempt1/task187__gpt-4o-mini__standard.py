import ast

def find_bare_excepts(source: str) -> list[int]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid Python source code")

    bare_except_lines = []

    class ExceptHandlerVisitor(ast.NodeVisitor):
        def visit_ExceptHandler(self, node: ast.ExceptHandler):
            if node.type is None:  # This means it's a bare except
                bare_except_lines.append(node.lineno)
            self.generic_visit(node)

    visitor = ExceptHandlerVisitor()
    visitor.visit(tree)

    return sorted(bare_except_lines)
