import ast

def find_mutable_defaults(source: str) -> list[tuple[str, int]]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise ValueError("Invalid Python source code")

    mutable_defaults = []

    class FunctionVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            if self.has_mutable_default(node):
                mutable_defaults.append((node.name, node.lineno))
            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node):
            if self.has_mutable_default(node):
                mutable_defaults.append((node.name, node.lineno))
            self.generic_visit(node)

        def has_mutable_default(self, node):
            for default in node.args.defaults + node.args.kw_defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    return True
            return False

    FunctionVisitor().visit(tree)
    return sorted(mutable_defaults, key=lambda x: (x[1], x[0]))
