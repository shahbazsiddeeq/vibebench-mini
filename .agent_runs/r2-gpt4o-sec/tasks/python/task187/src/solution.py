import ast

def find_bare_excepts(source: str) -> list[int]:
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError("Invalid Python source") from e

    bare_except_lines = []

    class BareExceptFinder(ast.NodeVisitor):
        def visit_ExceptHandler(self, node):
            if node.type is None:
                bare_except_lines.append(node.lineno)
            self.generic_visit(node)

    finder = BareExceptFinder()
    finder.visit(tree)

    return sorted(bare_except_lines)
